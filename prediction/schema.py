"""`Prediction`: the standard record for one text, what the runner, XAI methods and metrics see.

Decisions: 02_Decisions 2026-11-23 (#1 core contract, #6 provenance, #7 failures / off-label).
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

from data.schema import EMOTIONS

Status = Literal["ok", "off_label", "failed"]
SUM_TOL = 1e-9


@dataclass(frozen=True)
class Prediction:
    """Standardized prediction for one text.

    status: "ok" (label mass > 0), "off_label" (no label token at all), "failed" (call failed).
    probs: six renormalised probabilities in EMOTIONS order, sum 1; None unless ok.
    label_mass: sum of raw label probabilities; 0.0 for off_label, None for failed.
    label: argmax of probs (ties -> first in EMOTIONS); None unless ok.
    mass_partial: True if only top-k tokens were known (API): label_mass is a lower bound.
    Raw label probabilities are not stored (= probs * label_mass).
    """

    status: Status
    probs: tuple[float, ...] | None
    label_mass: float | None
    label: str | None
    mass_partial: bool
    error: str | None
    seconds: float
    n_input_tokens: int
    cache_hit: bool = False
    fingerprint: str | None = None

    def __post_init__(self) -> None:
        if self.status == "ok":
            if self.probs is None or len(self.probs) != len(EMOTIONS):
                raise ValueError("an ok Prediction needs six probabilities")
            if not math.isclose(sum(self.probs), 1.0, abs_tol=SUM_TOL):
                raise ValueError(f"probabilities must sum to 1, got {sum(self.probs)}")
            if self.label not in EMOTIONS:
                raise ValueError(f"an ok Prediction needs a label from EMOTIONS, got {self.label!r}")
            if self.label_mass is None or not 0.0 < self.label_mass <= 1.0 + SUM_TOL:
                raise ValueError(f"an ok Prediction needs label_mass in (0, 1], got {self.label_mass}")
        elif self.status in ("off_label", "failed"):
            if self.probs is not None or self.label is not None:
                raise ValueError(f"a {self.status} Prediction must not carry probs or a label")
            if self.status == "off_label" and self.label_mass != 0.0:
                raise ValueError("an off_label Prediction has label_mass 0.0")
            if self.status == "failed" and (self.error is None or self.label_mass is not None):
                raise ValueError("a failed Prediction needs an error and no label_mass")
        else:
            raise ValueError(f"unknown status {self.status!r}")

    @property
    def ok(self) -> bool:
        """True if the prediction has probabilities."""
        return self.status == "ok"

    def prob(self, emotion: str) -> float:
        """Renormalised probability of one emotion (an XAI method's target column)."""
        if not self.ok:
            raise ValueError(f"no probabilities: prediction status is {self.status!r}")
        return self.probs[EMOTIONS.index(emotion)]
