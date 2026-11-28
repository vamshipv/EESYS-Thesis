"""Tests for the Model Component contract and the FakeModel (plans/step01)."""
import math

import pytest

from data.schema import EMOTIONS
from models import Capabilities, FakeModel, RawOutput
from models.fake_model import CASE_SPLIT, DEFAULT_LEXICON, OFF_LABEL_TOKEN
from prompts import build_messages

HAPPY = "I am so happy today"


def prompts(*texts: str) -> list[list[dict]]:
    return [build_messages(t, "v3") for t in texts]


def score_one(model: FakeModel, text: str) -> RawOutput:
    return model.score(prompts(text))[0]


def emotion_share(out: RawOutput, emotion: str) -> float:
    d = dict(out.token_probs)
    return d[emotion] + d[emotion.capitalize()]


def label_mass(out: RawOutput) -> float:
    return sum(p for t, p in out.token_probs if t != OFF_LABEL_TOKEN)


def test_deterministic():
    model = FakeModel()
    batch = prompts(HAPPY, "I hate this", "")
    assert [(o.token_probs, o.n_input_tokens) for o in model.score(batch)] == \
           [(o.token_probs, o.n_input_tokens) for o in model.score(batch)]


def test_order_kept():
    texts = ["so angry", "wow really", "I miss you"]
    outs = FakeModel().score(prompts(*texts))
    winners = [max(EMOTIONS, key=lambda e: emotion_share(o, e)) for o in outs]
    assert winners == ["anger", "surprise", "sadness"]


def test_evidence_raises_share():
    model = FakeModel()
    with_word, without = score_one(model, HAPPY), score_one(model, "I am so today")
    assert max(EMOTIONS, key=lambda e: emotion_share(with_word, e)) == "joy"
    assert emotion_share(with_word, "joy") > emotion_share(without, "joy")
    assert emotion_share(with_word, "joy") == pytest.approx(0.618, abs=1e-3)
    assert label_mass(with_word) == pytest.approx(0.772, abs=1e-3)


def test_casings_split():
    d = dict(score_one(FakeModel(), HAPPY).token_probs)
    for e in EMOTIONS:
        assert d[e] / (d[e] + d[e.capitalize()]) == pytest.approx(CASE_SPLIT)


def test_probs_sum_to_one_and_sorted():
    out = score_one(FakeModel(), "I love it but I am scared")
    probs = [p for _, p in out.token_probs]
    assert len(out.token_probs) == 13
    assert math.isclose(sum(probs), 1.0, abs_tol=1e-9)
    assert probs == sorted(probs, reverse=True)


def test_empty_text():
    model = FakeModel()
    empty = score_one(model, "")
    shares = [emotion_share(empty, e) for e in EMOTIONS]
    assert all(s == pytest.approx(shares[0]) for s in shares)
    assert dict(empty.token_probs)[OFF_LABEL_TOKEN] == pytest.approx(0.552, abs=1e-3)
    assert label_mass(empty) < label_mass(score_one(model, HAPPY))


def test_fail_on():
    model = FakeModel(fail_on={"broken text"})
    ok1, bad, ok2 = model.score(prompts(HAPPY, "broken text", "so sad"))
    assert bad.failed and bad.token_probs == () and bad.error == "FakeModel: forced failure"
    assert not ok1.failed and not ok2.failed and len(ok1.token_probs) == 13


def test_raw_output_validation():
    with pytest.raises(ValueError):
        RawOutput((("joy", 0.5),), "complete", 0.0, 1, error="boom")
    with pytest.raises(ValueError):
        RawOutput((("joy", 1.5),), "complete", 0.0, 1)


def test_capabilities():
    assert FakeModel().capabilities == Capabilities(True, False, False, True)
    assert FakeModel().capabilities.enabled() == frozenset({"scores", "repeated_calls"})
    custom = Capabilities(scores=False, gradients=True, generation=True, repeated_calls=False)
    assert FakeModel(capabilities=custom).capabilities is custom
    assert custom.enabled() == frozenset({"gradients", "generation"})


def test_n_calls():
    model = FakeModel(fail_on={"x"})
    model.score(prompts("a", "x", "c"))
    model.score(prompts("d", "e"))
    assert model.n_calls == 5


def test_coverage_and_input_tokens():
    out = score_one(FakeModel(), "I'm so happy, really!")
    assert out.coverage == "complete"
    assert out.n_input_tokens == 4  # i'm, so, happy, really


def test_only_user_message_counts():
    model = FakeModel()
    other = [{"role": "system", "content": "angry furious hate"}, {"role": "user", "content": HAPPY}]
    assert model.score([other])[0].token_probs == score_one(model, HAPPY).token_probs
    with pytest.raises(ValueError):
        model.score([[{"role": "system", "content": "no user here"}]])


def test_lexicon_values_in_emotions():
    assert set(DEFAULT_LEXICON.values()) <= set(EMOTIONS)
    with pytest.raises(ValueError):
        FakeModel(lexicon={"calm": "neutral"})
