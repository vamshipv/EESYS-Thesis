"""Tests for the data module. Uses the cached validation split; writes only to tmp folders."""
import json
from collections import Counter

import pytest

from data.build_sample import build_sample, word_count
from data.loader import load_samples
from data.schema import EMOTIONS

DEV_ARGS = dict(split="validation", n_per_label=10, min_words=5, max_words=15)


def read(path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f]


@pytest.fixture(scope="module")
def seed42(tmp_path_factory):
    d = tmp_path_factory.mktemp("s42")
    return read(build_sample(**DEV_ARGS, seed=42, out_name="a", out_dir=d)), d


def test_same_seed_identical(seed42, tmp_path):
    again = read(build_sample(**DEV_ARGS, seed=42, out_name="b", out_dir=tmp_path))
    assert again == seed42[0]


def test_different_seed_differs(seed42, tmp_path):
    other = read(build_sample(**DEV_ARGS, seed=7, out_name="c", out_dir=tmp_path))
    assert {r["id"] for r in other} != {r["id"] for r in seed42[0]}


def test_nested(seed42, tmp_path):
    big = read(build_sample(**{**DEV_ARGS, "n_per_label": 20}, seed=42, out_name="big", out_dir=tmp_path))
    assert {r["id"] for r in seed42[0]} <= {r["id"] for r in big}


def test_only_single_label_target_emotions(seed42):
    import datasets
    from data.build_sample import CONFIG, DATASET, REVISION
    ds = datasets.load_dataset(DATASET, CONFIG, split="validation", revision=REVISION)
    names = ds.features["labels"].feature.names
    by_id = {r["id"]: r["labels"] for r in ds}
    for r in seed42[0]:
        assert r["label"] in EMOTIONS and r["label"] != "neutral"
        assert len(by_id[r["id"]]) == 1, f"{r['id']} is multi-label"
        assert names[by_id[r["id"]][0]] == r["label"]


def test_word_filter_and_counts(seed42):
    rows = seed42[0]
    assert all(5 <= word_count(r["text"]) <= 15 for r in rows)
    assert Counter(r["label"] for r in rows) == {e: 10 for e in EMOTIONS}


def test_no_overwrite(seed42):
    with pytest.raises(FileExistsError):
        build_sample(**DEV_ARGS, seed=42, out_name="a", out_dir=seed42[1])


def test_too_few_raises(tmp_path):
    with pytest.raises(ValueError, match="Too few"):
        build_sample(**{**DEV_ARGS, "n_per_label": 10_000}, seed=42, out_name="x", out_dir=tmp_path)


def test_test_split_guard(tmp_path):
    with pytest.raises(PermissionError):
        build_sample(split="test", n_per_label=1, seed=42, out_name="t", out_dir=tmp_path)
    assert not list(tmp_path.iterdir())


def test_load_dev():
    samples = load_samples("dev")
    assert len(samples) == 60
    assert Counter(s.label for s in samples) == {e: 10 for e in EMOTIONS}


def test_loader_rejects_bad_file(seed42, tmp_path):
    rows = seed42[0]
    (tmp_path / "bad.jsonl").write_text(
        "\n".join(json.dumps(r) for r in rows + rows[:1]), encoding="utf-8")
    (tmp_path / "bad.meta.json").write_text(json.dumps({"total": len(rows) + 1}), encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate"):
        load_samples("bad", samples_dir=tmp_path)


def test_load_dev_large_contains_dev():
    big = load_samples("dev_large")
    assert len(big) == 150
    assert Counter(s.label for s in big) == {e: 25 for e in EMOTIONS}
    assert {s.id for s in load_samples("dev")} <= {s.id for s in big}
