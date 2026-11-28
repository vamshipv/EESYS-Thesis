"""Tests for Standardized Prediction (plans/step02)."""
import pytest

from data.schema import EMOTIONS
from experiments.prompt_comparison import backends
from models import FakeModel, RawOutput
from prediction import LLAMA31_FIRST_TOKENS, LabelTokenRule, Prediction, standardize, standardize_batch
from prompts import build_messages

LLAMA = LabelTokenRule(LLAMA31_FIRST_TOKENS)
PLAIN = LabelTokenRule()


def raw(*pairs: tuple[str, float], coverage: str = "complete") -> RawOutput:
    return RawOutput(tuple(pairs), coverage, 0.5, 7)


def raw_probs(pred: Prediction) -> dict[str, float]:
    return {e: pred.prob(e) * pred.label_mass for e in EMOTIONS}


# 1
@pytest.mark.parametrize("token", [
    "anger", " Ang", "ANGER", "ang", "an", "f", "F", "ear", "Fear", "sad", "Sadness", "dis",
    "surpr", "joy", "Joy", "neutral", "Neutral", "Rel", "frustration", "<off_label>", "", "  ",
])
def test_rule_equals_reference(token):
    assert LLAMA.match(token) == backends.match_label(token, first_tokens=LLAMA31_FIRST_TOKENS)


# 2
def test_f_only_with_llama_table():
    assert LLAMA.match("f") == "fear"
    assert PLAIN.match("f") is None
    assert PLAIN.match("fear") == "fear"


def test_rule_rejects_unknown_label():
    with pytest.raises(ValueError):
        LabelTokenRule({"neu": "neutral"})


# 3
def test_casings_add_up():
    pred = standardize(raw(("anger", 0.6), ("Ang", 0.3), ("ANGER", 0.05)), LLAMA)
    assert raw_probs(pred)["anger"] == pytest.approx(0.95)
    assert pred.label_mass == pytest.approx(0.95)


# 4
@pytest.mark.parametrize("extra", [[("neutral", 0.2), ("Neutral", 0.1)], [("<off_label>", 0.3)]])
def test_non_labels_never_count(extra):
    base = [("joy", 0.5), ("sad", 0.2)]
    without, with_extra = standardize(raw(*base), LLAMA), standardize(raw(*base, *extra), LLAMA)
    assert raw_probs(with_extra) == pytest.approx(raw_probs(without))
    assert with_extra.label_mass == pytest.approx(without.label_mass)
    assert with_extra.label_mass == pytest.approx(0.7)


# 5
def test_worked_example():
    pred = standardize(raw(("joy", 0.60), ("sadness", 0.20), ("anger", 0.05), ("fear", 0.03),
                           ("surprise", 0.01), ("disgust", 0.01), ("relief", 0.10)), PLAIN)
    assert pred.status == "ok" and pred.label == "joy"
    assert pred.label_mass == pytest.approx(0.90)
    assert pred.prob("joy") == pytest.approx(0.667, abs=1e-3)
    assert sum(pred.probs) == pytest.approx(1.0)


# 6
def test_probs_in_emotions_order():
    pairs = [("surprise", 0.05), ("joy", 0.3), ("anger", 0.1), ("sadness", 0.2), ("fear", 0.15),
             ("disgust", 0.2)]
    a, b = standardize(raw(*pairs), PLAIN), standardize(raw(*reversed(pairs)), PLAIN)
    assert a.probs == b.probs
    assert a.probs == tuple(dict(pairs)[e] for e in EMOTIONS)  # mass is 1.0 here


# 7
def test_tie_goes_to_first_in_emotions():
    assert standardize(raw(("sadness", 0.4), ("anger", 0.4)), PLAIN).label == "anger"


# 8
def test_off_label():
    pred = standardize(raw(("neutral", 0.7), ("Rel", 0.3)), LLAMA)
    assert pred.status == "off_label" and pred.label_mass == 0.0
    assert pred.probs is None and pred.label is None
    with pytest.raises(ValueError):
        pred.prob("joy")


# 9
def test_failed():
    pred = standardize(RawOutput((), "complete", 1.2, 5, error="timeout"), LLAMA)
    assert pred.status == "failed" and pred.error == "timeout"
    assert pred.probs is None and pred.label is None and pred.label_mass is None
    assert pred.seconds == 1.2 and pred.n_input_tokens == 5


# 10
def test_mass_partial():
    assert standardize(raw(("joy", 0.9), coverage="top-k"), PLAIN).mass_partial
    assert not standardize(raw(("joy", 0.9)), PLAIN).mass_partial


# 11
def test_low_mass_stays_ok():
    pred = standardize(raw(("relief", 0.95), ("sad", 0.03), ("joy", 0.02)), LLAMA)
    assert pred.status == "ok" and pred.label == "sadness"
    assert pred.label_mass == pytest.approx(0.05)
    assert pred.prob("sadness") == pytest.approx(0.6)


# 12
@pytest.mark.parametrize("kwargs", [
    dict(status="ok", probs=None, label_mass=0.9, label="joy"),
    dict(status="ok", probs=(0.5, 0.1, 0.1, 0.1, 0.1, 0.0), label_mass=0.9, label="anger"),
    dict(status="ok", probs=(1.0, 0, 0, 0, 0, 0), label_mass=0.9, label=None),
    dict(status="failed", probs=None, label_mass=None, label=None),
    dict(status="off_label", probs=(1.0, 0, 0, 0, 0, 0), label_mass=0.0, label=None),
    dict(status="off_label", probs=None, label_mass=0.2, label=None),
])
def test_prediction_validation(kwargs):
    with pytest.raises(ValueError):
        Prediction(mass_partial=False, error=None, seconds=0.0, n_input_tokens=1, **kwargs)


# 13
def test_fake_model_end_to_end():
    texts = ["I am so happy today", "", "broken text", "so sad"]
    model = FakeModel(fail_on={"broken text"})
    happy, empty, bad, sad = standardize_batch(
        model.score([build_messages(t, "v3") for t in texts]), PLAIN)
    assert happy.status == "ok" and happy.label == "joy"
    assert happy.label_mass == pytest.approx(0.772, abs=1e-3)
    assert happy.prob("joy") == pytest.approx(0.618 / 0.772, abs=1e-3)
    assert empty.status == "ok" and empty.label_mass == pytest.approx(0.448, abs=1e-3)
    assert empty.probs == pytest.approx((1 / 6,) * 6)
    assert bad.status == "failed"
    assert sad.label == "sadness"


# 14
def test_llama_table_matches_tokenizer(monkeypatch):
    transformers = pytest.importorskip("transformers")
    from llama_hf_test import MODEL_ID, MODEL_REVISION
    try:
        tok = transformers.AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION,
                                                         local_files_only=True)
    except Exception as exc:  # tokenizer not cached on this machine
        pytest.skip(f"tokenizer not available offline: {exc}")
    monkeypatch.setattr(backends, "hf_tokenizer", lambda: tok)
    assert backends.label_first_tokens.__wrapped__() == LLAMA31_FIRST_TOKENS
