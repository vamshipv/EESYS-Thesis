"""Batching equivalence check runs (PLAN.md steps 3-4); one JSONL row per (condition, text).

python -m experiments.batching_check.run --conditions single_control bs1      (step 3, 20 texts)
python -m experiments.batching_check.run --conditions bs4 bs8                 (step 4, 150 texts)
Prompt v3, order O1, sample dev_large in the reference's order. Resumable: chunks whose texts
are all in the output file are skipped, so chunk boundaries stay the same after a restart.
"""
import argparse
import json
import time
from pathlib import Path

from data import load_samples
from experiments.batching_check.batch_scoring import (PADDING_SIDE, PAD_TOKEN, ChunkOOM,
                                                      chunks, pad_token_id, score_chunk)
from experiments.prompt_comparison.backends import MIN_TOKEN_CHARS, label_first_tokens, score_hf
from experiments.prompt_comparison.run import git_commit, now, prompt_hashes
from prompts import build_messages

RESULTS_DIR = Path(__file__).parent / "results"
OUT = RESULTS_DIR / "2026-11-23_hf_bf16_batch.jsonl"
VERSION = "v3"
SAMPLE = "dev_large"
# condition -> (batch size or None for the unchanged score_hf, default number of texts)
CONDITIONS = {"single_control": (None, 20), "bs1": (1, 20), "bs4": (4, 150), "bs8": (8, 150)}


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Batching equivalence check")
    ap.add_argument("--conditions", nargs="+", required=True, choices=list(CONDITIONS))
    ap.add_argument("--limit", type=int, default=None, help="override the number of texts")
    return ap.parse_args()


def done_keys(path: Path) -> set[tuple]:
    """(condition, id) of rows already written."""
    if not path.exists():
        return set()
    with open(path, encoding="utf-8") as f:
        return {(r["condition"], r["id"]) for r in map(json.loads, filter(str.strip, f))}


def score_single(messages_chunk: list[list[dict]]) -> tuple[list[dict], float]:
    """Unchanged score_hf on a chunk of one, in score_chunk's return shape."""
    assert len(messages_chunk) == 1
    r = dict(score_hf(messages_chunk[0]))
    seconds = r.pop("seconds")
    r["n_pad_tokens"] = 0
    return [r], seconds


def peak_gpu_gib() -> float | None:
    import torch
    return torch.cuda.max_memory_allocated() / 2**30 if torch.cuda.is_available() else None


def reset_peak() -> None:
    import torch
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()


def run_condition(cond: str, samples: list, done: set, f, cmeta: dict) -> None:
    """Score one condition chunk by chunk, appending rows; marks OOM in cmeta and returns."""
    bs, _ = CONDITIONS[cond]
    score_fn = score_single if bs is None else score_chunk
    all_chunks = chunks(samples, bs or 1)
    todo = [(ci, c) for ci, c in enumerate(all_chunks)
            if not all((cond, s.id) in done for s in c)]
    print(f"{cond}: {len(all_chunks) - len(todo)} chunks done, {len(todo)} to run", flush=True)
    reset_peak()
    t_start = time.perf_counter()
    for n, (ci, chunk) in enumerate(todo, 1):
        try:
            rows, seconds = score_fn([build_messages(s.text, VERSION) for s in chunk])
        except ChunkOOM as exc:
            print(f"{cond}: OOM in chunk {ci}: {exc}", flush=True)
            cmeta.update({"status": "OOM", "oom_chunk": ci, "error": str(exc)[:500]})
            return
        for s, r in zip(chunk, rows):
            if (cond, s.id) in done:
                continue
            row = {"condition": cond, "batch_size": bs or 1, "id": s.id, "text": s.text,
                   "gold": s.label, "probs": r["probs"], "label_mass": r["label_mass"],
                   "pred": r["pred"], "top_tokens": r["top_tokens"],
                   "n_input_tokens": r["n_input_tokens"], "n_pad_tokens": r["n_pad_tokens"],
                   "chunk_index": ci, "chunk_seconds": seconds,
                   "seconds_per_text": seconds / len(chunk)}
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        f.flush()
        eta = (time.perf_counter() - t_start) / n * (len(todo) - n)
        print(f"[{cond} {n}/{len(todo)}] chunk {ci} ({len(chunk)} texts) {seconds:.1f}s "
              f"| {seconds / len(chunk):.1f}s/text | ETA {eta / 60:.1f} min", flush=True)
    peak = peak_gpu_gib()
    if peak is not None:
        cmeta["peak_gpu_gib"] = max(peak, cmeta.get("peak_gpu_gib") or 0.0)
    cmeta["status"] = "done"


def main() -> None:
    args = parse_args()
    import torch
    import transformers
    from llama_hf_test import CPU_MEM, GPU_MEM, MODEL_ID, MODEL_REVISION, load_model

    all_samples = load_samples(SAMPLE)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    meta_path = OUT.with_suffix(".meta.json")
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    commit = git_commit()
    if commit.endswith("-dirty"):
        print(f"WARNING: working tree is dirty ({commit})")
    meta.setdefault("sessions", []).append({"start": now(), "args": vars(args),
                                            "git_commit": commit})
    meta.update({
        "sample": SAMPLE, "prompt_version": VERSION, "order_id": "O1",
        "prompt_hash": prompt_hashes([VERSION])[VERSION], "git_commit": commit,
        "model": {"id": MODEL_ID, "revision": MODEL_REVISION, "dtype": "bfloat16",
                  "max_memory": {"gpu": GPU_MEM, "cpu": CPU_MEM}},
        "pad_token": PAD_TOKEN, "pad_token_id": pad_token_id(), "padding_side": PADDING_SIDE,
        "position_ids": "attention_mask.cumsum(-1) - 1, clamped at 0",
        "batch_sizes": {c: CONDITIONS[c][0] for c in CONDITIONS},
        "label_token_rule": {"min_prefix_chars": MIN_TOKEN_CHARS,
                             "exact_first_tokens": label_first_tokens()},
        "torch": torch.__version__, "transformers": transformers.__version__,
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
    })
    meta.setdefault("conditions", {})

    def save_meta() -> None:
        meta["sessions"][-1]["end"] = now()
        meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    t0 = time.perf_counter()
    load_model()
    print(f"Model loaded in {time.perf_counter() - t0:.0f}s", flush=True)
    done = done_keys(OUT)
    with open(OUT, "a", encoding="utf-8") as f:
        for cond in args.conditions:
            n = args.limit or CONDITIONS[cond][1]
            cmeta = meta["conditions"].setdefault(cond, {})
            cmeta.update({"n_texts": n, "batch_size": CONDITIONS[cond][0]})
            run_condition(cond, all_samples[:n], done, f, cmeta)
            save_meta()
    save_meta()
    print(f"Done -> {OUT}")


if __name__ == "__main__":
    main()
