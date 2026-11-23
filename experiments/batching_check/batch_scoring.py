"""Batched bf16 Llama scoring: several prompts per forward pass, same label rule as score_hf.

Left padding (fixed correctness rule, 02_Decisions 2026-11-23): every row's last position is
its real last token, so logits[:, -1] is the next-token distribution for every row. Explicit
position_ids from the attention mask give real tokens the same positions as an unpadded run.
"""
import time
from functools import lru_cache
from typing import Callable

from experiments.prompt_comparison.backends import (hf_input_ids, hf_label_ids, hf_tokenizer,
                                                    summarise)

PAD_TOKEN = "<|finetune_right_pad_id|>"
PADDING_SIDE = "left"


class ChunkOOM(RuntimeError):
    """A chunk ran out of (GPU or CPU) memory; the batch size counts as failed ("OOM")."""


@lru_cache(maxsize=1)
def pad_token_id() -> int:
    """Id of PAD_TOKEN if it is in the vocab, else the eos token id (Llama 3.1 sets no pad)."""
    tok = hf_tokenizer()
    vocab = tok.get_vocab()
    if PAD_TOKEN in vocab:
        return vocab[PAD_TOKEN]
    eos = tok.eos_token_id
    return eos[0] if isinstance(eos, list) else eos


def render_batch(messages_list: list[list[dict]]) -> dict:
    """Left-padded batch of rendered chat prompts.

    Each prompt is rendered exactly as hf_input_ids does it, then padded on the left with
    pad_token_id(). Returns input_ids, attention_mask, position_ids (LongTensors,
    shape [n, max_len]) and n_pad (pad tokens per row).
    """
    import torch
    rows = [hf_input_ids(m)[0] for m in messages_list]
    width = max(len(r) for r in rows)
    pad = pad_token_id()
    input_ids = torch.full((len(rows), width), pad, dtype=torch.long)
    attention_mask = torch.zeros((len(rows), width), dtype=torch.long)
    for i, r in enumerate(rows):
        input_ids[i, width - len(r):] = r
        attention_mask[i, width - len(r):] = 1
    position_ids = (attention_mask.cumsum(-1) - 1).clamp(min=0)
    return {"input_ids": input_ids, "attention_mask": attention_mask,
            "position_ids": position_ids, "n_pad": [width - len(r) for r in rows]}


def _is_oom(exc: BaseException) -> bool:
    import torch
    return isinstance(exc, (torch.cuda.OutOfMemoryError, MemoryError)) or \
        "out of memory" in str(exc).lower()


def score_chunk(messages_chunk: list[list[dict]]) -> tuple[list[dict], float]:
    """One forward pass over a chunk. Returns (per-text dicts like score_hf, chunk seconds).

    Raises ChunkOOM if the pass runs out of memory.
    """
    import torch
    from llama_hf_test import load_model
    tok, model, _ = load_model()
    label_ids = hf_label_ids()
    label_set = {i for ids in label_ids.values() for i in ids}
    batch = render_batch(messages_chunk)
    inputs = {k: batch[k].to(model.device) for k in ("input_ids", "attention_mask", "position_ids")}
    t0 = time.perf_counter()
    try:
        with torch.no_grad():
            logits = model(**inputs).logits[:, -1].float()
    except (RuntimeError, MemoryError) as exc:
        if _is_oom(exc):
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            raise ChunkOOM(str(exc)) from exc
        raise
    seconds = time.perf_counter() - t0
    out = []
    for row, n_pad in zip(torch.softmax(logits, dim=-1), batch["n_pad"]):
        keep = label_set | set(row.topk(5).indices.tolist())
        pairs = sorted(((tok.decode([i]), row[i].item()) for i in keep), key=lambda x: -x[1])
        r = summarise(pairs, seconds)
        r.pop("seconds")
        r["n_input_tokens"] = batch["input_ids"].shape[1] - n_pad
        r["n_pad_tokens"] = n_pad
        out.append(r)
    return out, seconds


def chunks(items: list, size: int) -> list[list]:
    """Consecutive chunks of `size` (last one may be smaller)."""
    return [items[i:i + size] for i in range(0, len(items), size)]


def score_hf_batch(messages_list: list[list[dict]], batch_size: int,
                   score_fn: Callable = score_chunk) -> list[dict]:
    """Score all prompts in chunks of batch_size; one dict per prompt, in input order.

    Each dict has the score_hf fields (probs, label_mass, pred, top_tokens, n_input_tokens)
    plus n_pad_tokens, chunk_index, chunk_seconds and seconds_per_text.
    """
    results = []
    for ci, chunk in enumerate(chunks(messages_list, batch_size)):
        rows, seconds = score_fn(chunk)
        assert len(rows) == len(chunk), "scorer returned a different number of rows"
        for r in rows:
            results.append({**r, "chunk_index": ci, "chunk_seconds": seconds,
                            "seconds_per_text": seconds / len(chunk)})
    return results
