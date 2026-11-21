"""Check that a first token "f" really means "fear" on bf16 Llama (HF).

One forward pass per text with "f" appended after the assistant header gives both
P("f" | prompt) (logits before "f") and P(next | prompt + "f") (logits after "f").
Texts: all fear texts in `dev` + 2 per other emotion; versions v2 and v3 (lowercase prompts).

python -m experiments.prompt_comparison.check_fear_split
"""
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import torch

from data import load_samples
from data.schema import EMOTIONS
from experiments.prompt_comparison.backends import hf_input_ids, hf_tokenizer
from llama_hf_test import MODEL_ID, MODEL_REVISION, load_model
from prompts import build_messages

OUT = Path(__file__).parent / "results" / "2026-11-21_hf_fear_split_check.json"


def pick_texts() -> list:
    """All dev fear texts + the first 2 dev texts of every other emotion."""
    dev = load_samples("dev")
    other = [s for e in EMOTIONS if e != "fear" for s in [x for x in dev if x.label == e][:2]]
    return [s for s in dev if s.label == "fear"] + other


def check(text: str, version: str) -> dict:
    tok = hf_tokenizer()
    model = load_model()[1]
    f_id, ear_id = tok.encode("fear", add_special_tokens=False)
    ids = torch.cat([hf_input_ids(build_messages(text, version)), torch.tensor([[f_id]])], dim=1)
    t0 = time.perf_counter()
    with torch.no_grad():
        logits = model(ids.to(model.device)).logits[0, -2:].float()
    before, after = torch.softmax(logits, dim=-1)
    top_p, top_i = after.topk(5)
    return {"p_f": before[f_id].item(), "p_ear_given_f": after[ear_id].item(),
            "top_after_f": [{"token": tok.decode([i]), "prob": p}
                            for p, i in zip(top_p.tolist(), top_i.tolist())],
            "seconds": time.perf_counter() - t0}


def main() -> None:
    if OUT.exists():
        raise FileExistsError(f"{OUT} exists; not overwriting.")
    texts = pick_texts()
    rows = []
    for v in ("v2", "v3"):
        for n, s in enumerate(texts, 1):
            r = {"id": s.id, "text": s.text, "gold": s.label, "version": v, **check(s.text, v)}
            rows.append(r)
            print(f"[{v} {n}/{len(texts)}] {s.label:<8} P(f)={r['p_f']:.3f} "
                  f"P(ear|f)={r['p_ear_given_f']:.4f} {r['seconds']:.0f}s", flush=True)
    summary = {}
    for v in ("v2", "v3"):
        for group, keep in (("fear", lambda r: r["gold"] == "fear"), ("non-fear", lambda r: r["gold"] != "fear")):
            sel = [r for r in rows if r["version"] == v and keep(r)]
            summary[f"{v} {group}"] = {"n": len(sel),
                                       "min_p_ear_given_f": min(r["p_ear_given_f"] for r in sel),
                                       "mean_p_ear_given_f": sum(r["p_ear_given_f"] for r in sel) / len(sel),
                                       "mean_p_f": sum(r["p_f"] for r in sel) / len(sel)}
    OUT.write_text(json.dumps({"model": MODEL_ID, "revision": MODEL_REVISION, "dtype": "bfloat16",
                               "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                               "summary": summary, "rows": rows}, indent=2, ensure_ascii=False),
                   encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
