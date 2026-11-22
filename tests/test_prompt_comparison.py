"""Tests for the prompt-comparison helpers (no model calls)."""
from data.schema import EMOTIONS
from experiments.prompt_comparison.analyze import macro_f1, mcnemar_exact
from experiments.prompt_comparison.backends import label_first_tokens, match_label, summarise
from experiments.prompt_comparison.orders import ORDERS


def test_match_label_rule():
    assert match_label(" Sad") == "sadness"
    assert match_label("anger") == "anger"
    assert match_label("fe") is None and match_label("F") is None  # < 3 chars, not a first token
    assert match_label("f") == "fear"  # tokenizer splits lowercase "fear" into "f" + "ear"
    assert match_label("fear") == "fear" and match_label("joyful") is None
    assert match_label("sur") == "surprise" and match_label("the") is None


def test_summarise_mass_and_renorm():
    out = summarise([("joy", 0.6), ("Joy", 0.2), ("sad", 0.1), ("The", 0.1)], 0.0)
    assert abs(out["label_mass"] - 0.9) < 1e-9
    assert out["pred"] == "joy" and abs(out["probs"]["joy"] - 0.8 / 0.9) < 1e-9


def test_orders_are_rotations():
    assert ORDERS["O1"] == EMOTIONS and len(ORDERS) == 6
    for pos in range(6):
        assert sorted(o[pos] for o in ORDERS.values()) == sorted(EMOTIONS)


def test_mcnemar_exact():
    assert mcnemar_exact(0, 0) == 1.0
    assert abs(mcnemar_exact(0, 6) - 2 / 64) < 1e-12  # two-sided binomial, n=6
    assert mcnemar_exact(3, 3) == 1.0


def test_macro_f1_perfect():
    assert macro_f1(EMOTIONS * 2, EMOTIONS * 2)[0] == 1.0


def test_label_first_tokens():
    firsts = label_first_tokens()
    assert set(firsts.values()) == set(EMOTIONS)
    short = {t: l for t, l in firsts.items() if len(t.strip()) < 3}
    assert short == {"f": "fear"}  # the only split case


def _row(i, v, gold, pred, mass, o="O1"):
    return {"id": i, "version": v, "order_id": o, "gold": gold, "pred": pred,
            "correct": gold == pred, "label_mass": mass}


def test_mass_stats_cells():
    from experiments.prompt_comparison.analyze import mass_stats
    a = [_row(1, "a", "joy", "joy", 0.5), _row(2, "a", "joy", "joy", 0.5), _row(3, "a", "joy", "joy", 0.95)]
    b = [_row(1, "b", "joy", "joy", 0.99), _row(2, "b", "joy", "joy", 0.5), _row(3, "b", "joy", "joy", 0.8)]
    s = mass_stats(a, b)
    # text 1: low for a only; text 2: low for both; text 3: low for b only; b higher on text 1
    assert (s["a_only"], s["b_only"], s["both"], s["neither"], s["b_higher"]) == (1, 1, 1, 0, 1)


def test_merge_rejects_mismatch_and_duplicates():
    import pytest
    from pathlib import Path
    from experiments.prompt_comparison.analyze import merge
    m = {"backend": "hf", "model": {"id": "x"}, "sample": "dev_large"}
    r = [_row(1, "v1", "joy", "joy", 1.0)]
    with pytest.raises(ValueError, match="backend"):
        merge([(Path("a"), r, m), (Path("b"), [_row(1, "v2", "joy", "joy", 1.0)], {**m, "backend": "ollama"})])
    with pytest.raises(ValueError, match="both"):
        merge([(Path("a"), r, m), (Path("b"), r, m)])
