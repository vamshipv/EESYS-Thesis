"""Build reproducible, stratified GoEmotions samples.

Filtering: single-label texts whose label is one of EMOTIONS (neutral, multi-label and other
emotions are dropped), optionally within a word-count range.

Sampling is nested: per emotion, the filtered pool is sorted by id, shuffled once with a
seeded RNG and the first n_per_label are taken. With the same seed and filter, a larger sample
always contains the smaller one. Existing sample files are never overwritten.

Sets used in the thesis:
    dev   (built by running this file):
        build_sample(split="validation", n_per_label=10, seed=42,
                     min_words=5, max_words=15, out_name="dev")
    dev_large (prompt comparison, 2026-11-21, one-off command; contains dev):
        build_sample(split="validation", n_per_label=25, seed=42,
                     min_words=5, max_words=15, out_name="dev_large")
    final (later, NOT run from here):
        build_sample(split="test", n_per_label=50, seed=42,
                     out_name="final", allow_test=True)
"""
import json
import random
from datetime import datetime, timezone
from pathlib import Path

import datasets

from data.schema import EMOTIONS

DATASET = "google-research-datasets/go_emotions"
CONFIG = "simplified"
REVISION = "add492243ff905527e67aeb8b80c082af02207c3"  # pinned dataset commit
SAMPLES_DIR = Path(__file__).parent / "samples"


def word_count(text: str) -> int:
    """Whitespace word count (same rule as the earlier extract_goemotions.py)."""
    return len(text.split())


def load_pools(split: str, min_words: int | None, max_words: int | None) -> dict[str, list[dict]]:
    """Filtered records per emotion, sorted by id so order doesn't depend on the dataset."""
    ds = datasets.load_dataset(DATASET, CONFIG, split=split, revision=REVISION)
    names = ds.features["labels"].feature.names
    pools: dict[str, list[dict]] = {e: [] for e in EMOTIONS}
    for row in ds:
        if len(row["labels"]) != 1:
            continue
        label = names[row["labels"][0]]
        text = row["text"].strip()
        if label not in pools or not text:
            continue
        n = word_count(text)
        if (min_words is not None and n < min_words) or (max_words is not None and n > max_words):
            continue
        pools[label].append({"id": row["id"], "text": text, "label": label})
    for pool in pools.values():
        pool.sort(key=lambda r: r["id"])
    return pools


def draw(pools: dict[str, list[dict]], n_per_label: int, seed: int) -> list[dict]:
    """Nested stratified draw: shuffle each pool once with the seed, take the first n."""
    short = {e: len(p) for e, p in pools.items() if len(p) < n_per_label}
    if short:
        raise ValueError(f"Too few texts for n_per_label={n_per_label}: {short}")
    out = []
    for emotion in EMOTIONS:
        pool = list(pools[emotion])
        random.Random(f"{seed}:{emotion}").shuffle(pool)
        out.extend(pool[:n_per_label])
    return out


def build_sample(
    split: str,
    n_per_label: int,
    seed: int,
    min_words: int | None = None,
    max_words: int | None = None,
    out_name: str = "dev",
    allow_test: bool = False,
    out_dir: Path = SAMPLES_DIR,
) -> Path:
    """Build and write <out_dir>/<out_name>.jsonl plus .meta.json. Returns the jsonl path.

    Raises PermissionError for split="test" without allow_test=True, FileExistsError if the
    sample already exists, ValueError if an emotion has fewer than n_per_label texts.
    """
    if split == "test" and not allow_test:
        raise PermissionError("Test split is reserved for the final set; pass allow_test=True.")
    out_dir = Path(out_dir)
    jsonl, meta_path = out_dir / f"{out_name}.jsonl", out_dir / f"{out_name}.meta.json"
    if jsonl.exists() or meta_path.exists():
        raise FileExistsError(f"{jsonl} already exists; use a new out_name.")

    pools = load_pools(split, min_words, max_words)
    records = draw(pools, n_per_label, seed)

    out_dir.mkdir(parents=True, exist_ok=True)
    with open(jsonl, "x", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    meta = {
        "name": out_name,
        "dataset": DATASET,
        "config": CONFIG,
        "revision": REVISION,
        "datasets_version": datasets.__version__,
        "split": split,
        "seed": seed,
        "n_per_label": n_per_label,
        "word_filter": {"min_words": min_words, "max_words": max_words},
        "available_per_emotion": {e: len(pools[e]) for e in EMOTIONS},
        "sampled_per_emotion": {e: n_per_label for e in EMOTIONS},
        "total": len(records),
        "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    with open(meta_path, "x", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    return jsonl


if __name__ == "__main__":
    path = build_sample(split="validation", n_per_label=10, seed=42,
                        min_words=5, max_words=15, out_name="dev")
    print(f"Wrote {path}")
