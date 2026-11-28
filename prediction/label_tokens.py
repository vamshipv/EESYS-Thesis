"""Label-token rule: which first answer token counts for which emotion.

Copy of `experiments/prompt_comparison/backends.match_label` (the rule frozen with prompt v3),
moved here so every component is scored by one implementation.
Decisions: 02_Decisions 2026-11-21 (label-token rule, the "f" fix), 2026-11-23 (#7).
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType

from data.schema import EMOTIONS

MIN_TOKEN_CHARS = 3

# Llama 3.1 tokenizer's own first token of each label, lowercase and capitalised -> label.
# Derived once with backends.label_first_tokens() from unsloth/Llama-3.1-8B-Instruct,
# revision 4699cc75b550f9c6f3173fb80f4703b62d946aa5, on 2026-11-28. Do not edit by hand.
LLAMA31_FIRST_TOKENS: dict[str, str] = {
    "anger": "anger", "Ang": "anger",
    "dis": "disgust", "Dis": "disgust",
    "f": "fear", "Fear": "fear",
    "joy": "joy", "Joy": "joy",
    "sad": "sadness", "Sad": "sadness",
    "sur": "surprise", "Sur": "surprise",
}


@dataclass(frozen=True)
class LabelTokenRule:
    """Maps a first answer token to the emotion it counts for (or None).

    A token counts for a label if (a) after strip + lower it has at least MIN_TOKEN_CHARS
    characters and the label starts with it ("anger", " Ang", "sad"), or (b) it is exactly one
    of the model tokenizer's own first tokens of a label (`first_tokens`, e.g. "f" for fear).

    first_tokens: per-model table, token -> label (empty for FakeModel).
    rule_id: version of the rule; goes into the setup fingerprint.
    """

    first_tokens: Mapping[str, str] = field(default_factory=dict)
    rule_id: str = "label-token-v2"

    def __post_init__(self) -> None:
        unknown = set(self.first_tokens.values()) - set(EMOTIONS)
        if unknown:
            raise ValueError(f"first_tokens map to unknown labels: {sorted(unknown)}")
        object.__setattr__(self, "first_tokens", MappingProxyType(dict(self.first_tokens)))

    def match(self, token: str) -> str | None:
        """Label the token counts for, or None (non-label tokens such as "neutral")."""
        if token in self.first_tokens:
            return self.first_tokens[token]
        t = token.strip().lower()
        if len(t) < MIN_TOKEN_CHARS:
            return None
        hits = [label for label in EMOTIONS if label.startswith(t)]
        assert len(hits) <= 1, f"token {token!r} matches several labels {hits}"
        return hits[0] if hits else None
