"""Shared contract for all Model Components (Exposé Figure 1: Local / Online Model Component).

Components return RAW outputs only: (token, probability) pairs for the first answer token.
Turning tokens into emotions (label-token rule, label mass, renormalising) is the job of
Standardized Prediction (`prediction/`), so it exists once for every component.
Decisions: 02_Decisions 2026-11-23 (#7 common interface), 2026-11-24 (capability flags).
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from typing import Literal

Coverage = Literal["complete", "top-k"]


@dataclass(frozen=True)
class Capabilities:
    """What a component CAN do (its "has"), declared once per component.

    Access levels are not set here: the Model Interface switches flags off per config.
    """

    scores: bool
    gradients: bool
    generation: bool
    repeated_calls: bool

    def enabled(self) -> frozenset[str]:
        """Names of the flags that are True (for `needs <= allowed` checks)."""
        return frozenset(f.name for f in fields(self) if getattr(self, f.name))


@dataclass(frozen=True)
class RawOutput:
    """Raw result of one component call for ONE text. Same shape for every component.

    token_probs: (token string, probability), highest probability first.
    coverage: "complete" if every relevant token is present (Llama, FakeModel),
        "top-k" if only the API's top-k logprobs are known.
    A failed call has an `error` and no probabilities (never zeros or uniform values).
    """

    token_probs: tuple[tuple[str, float], ...]
    coverage: Coverage
    seconds: float
    n_input_tokens: int
    error: str | None = None

    def __post_init__(self) -> None:
        if self.error is not None and self.token_probs:
            raise ValueError("a failed RawOutput must not carry probabilities")
        for token, prob in self.token_probs:
            if not 0.0 <= prob <= 1.0:
                raise ValueError(f"probability of {token!r} outside [0, 1]: {prob}")

    @property
    def failed(self) -> bool:
        """True if the call failed (an error is set)."""
        return self.error is not None


class ModelComponent(ABC):
    """Base class for Model Components (FakeModel, OllamaModel, LlamaHFModel, online model).

    A component receives already-built chat prompts and returns raw token probabilities.
    It never builds prompts and never sees sample ids, gold labels, prompt version or
    label order; it knows nothing about emotions as classes.
    """

    capabilities: Capabilities
    model_id: str

    @abstractmethod
    def score(self, messages_batch: list[list[dict]]) -> list[RawOutput]:
        """Score a list of chat prompts (each the messages from `prompts.build_messages`).

        Returns one RawOutput per prompt, in the same order. A failure for one text gives
        a failed RawOutput for that text and the others still come back; only programmer
        errors (e.g. a prompt without a user message) raise.
        """
