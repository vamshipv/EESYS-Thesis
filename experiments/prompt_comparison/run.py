"""Run prompt versions x label orders over a sample on one backend; one JSONL row per call.

python -m experiments.prompt_comparison.run --backend ollama --versions v1 v2 v3 [--orders O1]
    [--sample dev_large] [--limit N] [--tag dryrun]
Resumable: rows already in the output file (same id, version, order_id) are skipped.
"""
import argparse
import hashlib
import json
import subprocess
import time
from datetime import date, datetime, timezone
from pathlib import Path

from data import load_samples
from experiments.prompt_comparison.backends import MIN_TOKEN_CHARS, label_first_tokens
from experiments.prompt_comparison.orders import ORDERS
from prompts import PROMPTS_DIR, build_messages

RESULTS_DIR = Path(__file__).parent / "results"


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Prompt comparison run")
    ap.add_argument("--backend", choices=["ollama", "hf"], required=True)
    ap.add_argument("--sample", default="dev_large")
    ap.add_argument("--versions", nargs="+", required=True)
    ap.add_argument("--orders", nargs="+", default=["O1"], choices=list(ORDERS))
    ap.add_argument("--limit", type=int, default=None, help="first N texts only")
    ap.add_argument("--tag", default=None)
    ap.add_argument("--model", default="llama3.1", help="Ollama model name")
    return ap.parse_args()


def git_commit() -> str:
    """Current commit of the code repo, with '-dirty' if there are uncommitted changes."""
    try:
        head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True,
                              text=True, check=True).stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain"], capture_output=True,
                               text=True).stdout.strip()
        return head + ("-dirty" if dirty else "")
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def prompt_hashes(versions: list[str]) -> dict[str, str]:
    """Short sha256 of each prompt file, so a run is tied to the exact template text."""
    return {v: hashlib.sha256((PROMPTS_DIR / f"{v}.txt").read_bytes()).hexdigest()[:12]
            for v in versions}


def backend_setup(args) -> tuple:
    """(score function, model id string, model/decoding info for the meta file)."""
    if args.backend == "ollama":
        from experiments.prompt_comparison.backends import (OLLAMA_OPTIONS, OLLAMA_TOP_K,
                                                            ollama_model_info, score_ollama)
        info = ollama_model_info(args.model)
        return (lambda m: score_ollama(m, args.model), f"ollama:{info['name']}",
                {"model": info, "decoding": {**OLLAMA_OPTIONS, "top_logprobs": OLLAMA_TOP_K}})
    from experiments.prompt_comparison.backends import score_hf
    from llama_hf_test import CPU_MEM, GPU_MEM, MODEL_ID, MODEL_REVISION
    return (score_hf, f"hf:{MODEL_ID}",
            {"model": {"id": MODEL_ID, "revision": MODEL_REVISION, "dtype": "bfloat16",
                       "max_memory": {"gpu": GPU_MEM, "cpu": CPU_MEM}},
             "decoding": "single forward pass, full next-token distribution (no sampling)"})


def done_keys(path: Path) -> set[tuple]:
    """(id, version, order_id) of rows already written."""
    if not path.exists():
        return set()
    with open(path, encoding="utf-8") as f:
        return {(r["id"], r["version"], r["order_id"])
                for r in map(json.loads, filter(str.strip, f))}


def output_path(args) -> Path:
    """Reuse the newest file with this backend+tag (resume), else start one dated today."""
    suffix = f"_{args.backend}" + (f"_{args.tag}" if args.tag else "")
    existing = sorted(RESULTS_DIR.glob(f"*{suffix}.jsonl"))
    return existing[-1] if existing else RESULTS_DIR / f"{date.today().isoformat()}{suffix}.jsonl"


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def main() -> None:
    args = parse_args()
    samples = load_samples(args.sample)[: args.limit]
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out = output_path(args)
    meta_path = out.with_suffix(".meta.json")
    done = done_keys(out)
    jobs = [(s, v, o) for v in args.versions for o in args.orders for s in samples
            if (s.id, v, o) not in done]
    print(f"{out.name}: {len(done)} rows already done, {len(jobs)} to run")
    if not jobs:
        return

    score, model_id, info = backend_setup(args)
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    meta.setdefault("sessions", []).append({"start": now(), "args": vars(args)})
    meta.update({"sample": args.sample, "limit": args.limit, "backend": args.backend,
                 "versions": sorted(set(meta.get("versions", [])) | set(args.versions)),
                 "orders": sorted(set(meta.get("orders", [])) | set(args.orders)),
                 "prompt_hashes": {**meta.get("prompt_hashes", {}), **prompt_hashes(args.versions)},
                 "git_commit": git_commit(), **info,
                 "label_token_rule": {"min_prefix_chars": MIN_TOKEN_CHARS,
                                      "exact_first_tokens": label_first_tokens()}})

    t_start = time.perf_counter()
    with open(out, "a", encoding="utf-8") as f:
        for n, (s, v, o) in enumerate(jobs, 1):
            r = score(build_messages(s.text, v, labels=ORDERS[o]))
            row = {"id": s.id, "text": s.text, "gold": s.label, "version": v, "order_id": o,
                   "labels_order": ORDERS[o], "pred": r["pred"], "correct": r["pred"] == s.label,
                   "probs": r["probs"], "label_mass": r["label_mass"],
                   "top_tokens": r["top_tokens"], "seconds": r["seconds"],
                   "backend": args.backend, "model": model_id}
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            f.flush()
            eta = (time.perf_counter() - t_start) / n * (len(jobs) - n)
            print(f"[{n}/{len(jobs)}] {v} {o} | gold={s.label:<8} pred={r['pred']:<8} "
                  f"{'ok' if row['correct'] else 'XX'} mass={r['label_mass']:.2f} | "
                  f"{r['seconds']:.1f}s | ETA {eta / 60:.1f} min", flush=True)
            if n == 1 or n % 25 == 0 or n == len(jobs):  # a stopped run still has its meta
                meta["sessions"][-1]["end"] = now()
                meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Done in {(time.perf_counter() - t_start) / 60:.1f} min -> {out}")


if __name__ == "__main__":
    main()
