"""Hardware test: Llama 3.1 8B Instruct via Hugging Face transformers, full bf16 (no quantization).

The model (~16 GB) doesn't fit in 8 GB of video memory, so accelerate spreads it over
GPU -> CPU RAM -> disk. Expect slow predictions; this only checks that the setup runs.

Same prompt and same return format as ollama_calls_test.predict_proba, but the scores come
from the full next-token distribution instead of Ollama's top-20 logprobs.

Run:  python llama_hf_test.py [n_texts]      (default 3 dev-set texts)
Env overrides: LLAMA_MODEL_ID, LLAMA_GPU_MEM, LLAMA_CPU_MEM, LLAMA_OFFLOAD_DIR
"""
import math
import os
import sys
import time
from dataclasses import asdict
from functools import lru_cache
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from data import load_samples

LABELS = ["anger", "disgust", "fear", "joy", "sadness", "surprise"]
MODEL_ID = os.environ.get("LLAMA_MODEL_ID", "meta-llama/Llama-3.1-8B-Instruct")
GPU_MEM = os.environ.get("LLAMA_GPU_MEM", "6.5GiB")   # leave headroom on the 8 GB card
CPU_MEM = os.environ.get("LLAMA_CPU_MEM", "6GiB")     # 16 GB RAM total; rest goes to disk
# Outside OneDrive on purpose: several GB of offloaded weights shouldn't sync.
OFFLOAD_DIR = Path(os.environ.get("LLAMA_OFFLOAD_DIR", Path.home() / ".cache" / "llama_offload"))


def build_prompt(text: str) -> str:
    """Same prompt text as ollama_calls_test.py, so the two backends are comparable."""
    return (
        "Classify the emotion of the text. Answer with exactly one word from: "
        + ", ".join(LABELS) + ".\n\nText: " + text + "\nEmotion:"
    )


@lru_cache(maxsize=1)
def load_model() -> tuple:
    """Load tokenizer + bf16 model once per process, offloading what doesn't fit on the GPU."""
    OFFLOAD_DIR.mkdir(parents=True, exist_ok=True)
    tok = AutoTokenizer.from_pretrained(MODEL_ID)
    max_memory = {"cpu": CPU_MEM}
    if torch.cuda.is_available():
        max_memory[0] = GPU_MEM
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        max_memory=max_memory,
        offload_folder=str(OFFLOAD_DIR),
        low_cpu_mem_usage=True,
    )
    model.eval()
    return tok, model, label_token_ids(tok)


def label_token_ids(tok) -> dict[str, list[int]]:
    """First token id of each label, lower- and capitalised ("sad", "Sad", ...).

    The answer starts right after the assistant header, so there's no leading space.
    First tokens shorter than 3 characters are dropped (lowercase "fear" starts with
    just "f", which would also catch unrelated words).
    """
    ids = {}
    for l in LABELS:
        firsts = {tok.encode(v, add_special_tokens=False)[0] for v in (l, l.capitalize())}
        ids[l] = sorted(i for i in firsts if len(tok.decode([i]).strip()) >= 3)
        assert ids[l], f"no usable first token for {l}"
    flat = [i for v in ids.values() for i in v]
    assert len(flat) == len(set(flat)), f"labels share a first token: {ids}"
    return ids


def predict_details(text: str) -> dict:
    """One forward pass. Returns probs (6 labels, renormalised), top-5 tokens,
    label_mass (share of the full distribution on label tokens), seconds."""
    tok, model, label_ids = load_model()
    messages = [{"role": "user", "content": build_prompt(text)}]
    input_ids = tok.apply_chat_template(
        messages, add_generation_prompt=True, return_tensors="pt"
    ).to(model.device)

    t0 = time.perf_counter()
    with torch.no_grad():
        logits = model(input_ids).logits[0, -1].float()
    seconds = time.perf_counter() - t0

    logp = torch.log_softmax(logits, dim=-1)
    raw = {l: sum(math.exp(logp[i].item()) for i in ids) for l, ids in label_ids.items()}
    mass = sum(raw.values())
    probs = {l: s / (mass or 1.0) for l, s in raw.items()}
    top_lp, top_id = logp.topk(5)
    top = [{"token": tok.decode([i]), "logprob": lp} for lp, i in zip(top_lp.tolist(), top_id.tolist())]
    return {"probs": probs, "top": top, "label_mass": mass, "seconds": seconds,
            "n_input_tokens": input_ids.shape[1]}


def predict_proba(text: str, model: str = MODEL_ID) -> tuple[dict, list]:
    """Drop-in for ollama_calls_test.predict_proba: (6-label probs, top-5 first tokens)."""
    d = predict_details(text)
    return d["probs"], d["top"]


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    rows = [asdict(s) for s in load_samples("dev")][:n]  # shared dev set (validation split)

    t0 = time.perf_counter()
    _, model, _ = load_model()
    print(f"Loaded {MODEL_ID} in {time.perf_counter() - t0:.0f}s")
    placement = {}
    for dev in model.hf_device_map.values():
        placement[str(dev)] = placement.get(str(dev), 0) + 1
    print(f"Layer placement (modules per device): {placement}")

    for i, row in enumerate(rows, 1):
        d = predict_details(row["text"])
        pred = max(d["probs"], key=d["probs"].get)
        print("=" * 70)
        print(f"{i}. {row['text']}")
        print(f"   true {row['label']:<9} pred {pred:<9} ({d['probs'][pred]:.0%})  "
              f"{'CORRECT' if pred == row['label'] else 'WRONG'}")
        print(f"   {d['seconds']:.1f}s, {d['n_input_tokens']} input tokens, "
              f"label mass {d['label_mass']:.1%}")
        print("   top tokens: " + ", ".join(f"{t['token']!r} {math.exp(t['logprob']):.1%}" for t in d["top"]))
    if torch.cuda.is_available():
        print(f"Peak GPU memory: {torch.cuda.max_memory_allocated() / 2**30:.1f} GiB")
