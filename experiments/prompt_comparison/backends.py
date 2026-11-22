"""Score one chat prompt on Ollama or HF transformers with the same label-matching rule.

Both return: probs (6 labels, renormalised), label_mass (probability share on label tokens
before renormalising; Ollama: top-20 logprobs only), top_tokens (top 5), pred, seconds.
"""
import math
import time
from functools import lru_cache

import requests

from data.schema import EMOTIONS

OLLAMA_URL = "http://localhost:11434"
OLLAMA_TOP_K = 20
OLLAMA_RETRIES = 3  # attempts per call on HTTP 5xx
MIN_TOKEN_CHARS = 3


@lru_cache(maxsize=1)
def hf_tokenizer():
    """Llama 3.1 tokenizer only (no weights); also the source of first tokens for Ollama."""
    from transformers import AutoTokenizer
    from llama_hf_test import MODEL_ID, MODEL_REVISION
    return AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION)


@lru_cache(maxsize=1)
def label_first_tokens() -> dict[str, str]:
    """Exact first token string of each label as the tokenizer writes it, lower and
    capitalised (e.g. "f" for "fear", "Fear" for "Fear") -> label. Asserts no two labels
    share a first token."""
    tok = hf_tokenizer()
    out: dict[str, str] = {}
    for l in EMOTIONS:
        for form in (l, l.capitalize()):
            first = tok.decode([tok.encode(form, add_special_tokens=False)[0]])
            assert out.get(first, l) == l, f"{l} and {out[first]} share first token {first!r}"
            out[first] = l
    return out


def match_label(token: str, first_tokens: dict[str, str] | None = None) -> str | None:
    """Label a first answer token counts for, else None. It counts if (a) after strip+lower
    it has at least MIN_TOKEN_CHARS characters and a label starts with it ("sad", " Ang"),
    or (b) it is exactly the tokenizer's own first token of a label (adds "f" for fear)."""
    first_tokens = label_first_tokens() if first_tokens is None else first_tokens
    if token in first_tokens:
        return first_tokens[token]
    t = token.strip().lower()
    if len(t) < MIN_TOKEN_CHARS:
        return None
    hits = [l for l in EMOTIONS if l.startswith(t)]
    assert len(hits) <= 1, f"token {token!r} matches several labels {hits}"
    return hits[0] if hits else None


def summarise(token_probs: list[tuple[str, float]], seconds: float, top_n: int = 5) -> dict:
    """Shared result dict from (token, probability) pairs sorted by probability, highest first."""
    raw = {l: 0.0 for l in EMOTIONS}
    for tok, p in token_probs:
        if (l := match_label(tok)) is not None:
            raw[l] += p
    mass = sum(raw.values())
    probs = {l: s / mass if mass else 1 / len(EMOTIONS) for l, s in raw.items()}
    return {
        "probs": probs,
        "label_mass": mass,
        "top_tokens": [{"token": t, "prob": p} for t, p in token_probs[:top_n]],
        "pred": max(EMOTIONS, key=probs.get),  # ties -> first in EMOTIONS order
        "seconds": seconds,
    }


# --- Ollama -----------------------------------------------------------------------------

OLLAMA_OPTIONS = {"temperature": 0, "num_predict": 3}


def score_ollama(messages: list[dict], model: str = "llama3.1") -> dict:
    """One /api/chat call; scores labels from the first generated token's top-20 logprobs."""
    payload = {"model": model, "messages": messages, "stream": False, "think": False,
               "logprobs": True, "top_logprobs": OLLAMA_TOP_K, "options": OLLAMA_OPTIONS}
    for attempt in range(OLLAMA_RETRIES):
        t0 = time.perf_counter()
        r = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=300)
        seconds = time.perf_counter() - t0
        # Ollama can return 500 on the first request while it is still loading the model.
        if r.status_code < 500 or attempt == OLLAMA_RETRIES - 1:
            break
        time.sleep(5)
    r.raise_for_status()
    first = r.json()["logprobs"][0]["top_logprobs"]
    pairs = sorted(((t["token"], math.exp(t["logprob"])) for t in first), key=lambda x: -x[1])
    return summarise(pairs, seconds)


def ollama_model_info(model: str = "llama3.1") -> dict:
    """Digest and quantization of the local Ollama model, for the run's meta file."""
    tags = requests.get(f"{OLLAMA_URL}/api/tags", timeout=10).json()["models"]
    m = next(m for m in tags if m["name"].split(":")[0] == model.split(":")[0])
    return {"name": m["name"], "digest": m["digest"], **m["details"]}


# --- HF transformers ---------------------------------------------------------------------

@lru_cache(maxsize=1)
def hf_label_ids() -> dict[str, list[int]]:
    """All vocab ids that match_label assigns to each label (same rule as Ollama)."""
    tok = hf_tokenizer()
    ids: dict[str, list[int]] = {l: [] for l in EMOTIONS}
    for i in range(len(tok)):
        if (l := match_label(tok.decode([i]))) is not None:
            ids[l].append(i)
    return ids


def hf_input_ids(messages: list[dict]):
    """Token ids of the rendered Llama 3.1 chat prompt (with assistant header)."""
    return hf_tokenizer().apply_chat_template(messages, add_generation_prompt=True,
                                   return_tensors="pt", return_dict=True)["input_ids"]


def score_hf(messages: list[dict]) -> dict:
    """One forward pass of bf16 Llama; scores labels from the full next-token distribution."""
    import torch
    from llama_hf_test import load_model
    tok, model, _ = load_model()
    label_ids = hf_label_ids()
    input_ids = hf_input_ids(messages).to(model.device)
    t0 = time.perf_counter()
    with torch.no_grad():
        logits = model(input_ids).logits[0, -1].float()
    seconds = time.perf_counter() - t0
    p = torch.softmax(logits, dim=-1)
    # label tokens + overall top 5; summarise only needs the label tokens to be present
    keep = {i for ids in label_ids.values() for i in ids} | set(p.topk(5).indices.tolist())
    pairs = sorted(((tok.decode([i]), p[i].item(), i) for i in keep), key=lambda x: -x[1])
    out = summarise([(t, q) for t, q, _ in pairs], seconds)
    out["n_input_tokens"] = int(input_ids.shape[1])
    return out
