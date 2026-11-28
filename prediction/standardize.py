"""Raw component output -> standard `Prediction`. One implementation for every component.

Same arithmetic as `experiments/prompt_comparison/backends.summarise`, except that mass 0 gives
status "off_label" instead of uniform 1/6 (02_Decisions 2026-11-23, #7).
Knows nothing about prompts, models, targets or callers.
"""
from __future__ import annotations

from data.schema import EMOTIONS
from models.base import RawOutput
from prediction.label_tokens import LabelTokenRule
from prediction.schema import Prediction


def raw_label_probs(raw: RawOutput, rule: LabelTokenRule) -> dict[str, float]:
    """Sum of token probabilities per label (EMOTIONS order); non-label tokens are ignored."""
    sums = {label: 0.0 for label in EMOTIONS}
    for token, p in raw.token_probs:
        if (label := rule.match(token)) is not None:
            sums[label] += p
    return sums


def standardize(raw: RawOutput, rule: LabelTokenRule) -> Prediction:
    """Turn one RawOutput into a Prediction (failed / off_label / ok)."""
    common = dict(mass_partial=raw.coverage == "top-k", seconds=raw.seconds,
                  n_input_tokens=raw.n_input_tokens)
    if raw.failed:
        return Prediction(status="failed", probs=None, label_mass=None, label=None,
                          error=raw.error, **common)
    sums = raw_label_probs(raw, rule)
    mass = sum(sums.values())
    if mass == 0.0:
        return Prediction(status="off_label", probs=None, label_mass=0.0, label=None,
                          error=None, **common)
    probs = tuple(sums[label] / mass for label in EMOTIONS)
    label = EMOTIONS[probs.index(max(probs))]  # ties -> first in EMOTIONS order
    return Prediction(status="ok", probs=probs, label_mass=mass, label=label, error=None,
                      **common)


def standardize_batch(raws: list[RawOutput], rule: LabelTokenRule) -> list[Prediction]:
    """Standardize a list of RawOutputs, same order."""
    return [standardize(raw, rule) for raw in raws]
