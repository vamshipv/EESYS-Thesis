"""The one loader the rest of the pipeline uses for fixed samples."""
import json
from collections import Counter
from pathlib import Path

from data.schema import EMOTIONS, Sample

SAMPLES_DIR = Path(__file__).parent / "samples"


def load_samples(name: str, samples_dir: Path = SAMPLES_DIR) -> list[Sample]:
    """Read <samples_dir>/<name>.jsonl as Samples, validated against <name>.meta.json.

    Raises ValueError on duplicate ids, empty texts, unknown labels, unequal counts per
    emotion, or a total that doesn't match the meta file.
    """
    samples_dir = Path(samples_dir)
    with open(samples_dir / f"{name}.jsonl", encoding="utf-8") as f:
        samples = [Sample(**{k: r[k] for k in ("id", "text", "label")})
                   for r in map(json.loads, filter(str.strip, f))]
    with open(samples_dir / f"{name}.meta.json", encoding="utf-8") as f:
        meta = json.load(f)

    ids = Counter(s.id for s in samples)
    if dupes := [i for i, c in ids.items() if c > 1]:
        raise ValueError(f"{name}: duplicate ids {dupes}")
    if empty := [s.id for s in samples if not s.text.strip()]:
        raise ValueError(f"{name}: empty texts {empty}")
    if bad := {s.label for s in samples} - set(EMOTIONS):
        raise ValueError(f"{name}: labels not in EMOTIONS {bad}")
    counts = Counter(s.label for s in samples)
    if len({counts[e] for e in EMOTIONS}) != 1:
        raise ValueError(f"{name}: unequal counts per emotion {dict(counts)}")
    if len(samples) != meta["total"]:
        raise ValueError(f"{name}: {len(samples)} samples, meta says {meta['total']}")
    return samples
