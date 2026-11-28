"""FakeModel: a test-only Model Component with hand-written word rules.

It replaces Llama's neural network with a word list, so tests know the right explanation
in advance. It never produces thesis results; real runs use LlamaHFModel / the online
component, which have no lexicon.

Two different word lists:
- the LEXICON = words in the INPUT sentence that drive the fake decision ("happy");
- the LABEL TOKENS = the OUTPUT answer tokens ("joy" / "Joy", like Llama's "anger" / "Ang"),
  which Standardized Prediction maps to emotions for every component alike.

No "neutral": the off-label token is not an emotion class. It stands for everything the
model says that is not one of the six labels (the share `label_mass` leaves out), so the
low-mass / off_label handling in Standardized Prediction can be tested.
"""
from __future__ import annotations

import math
import re
import time
from collections import Counter
from collections.abc import Iterable, Mapping

from data.schema import EMOTIONS
from models.base import Capabilities, ModelComponent, RawOutput

WORD_WEIGHT = 3.0  # logit added to an emotion per matching lexicon word in the text
OFF_LABEL_TOKEN = "<off_label>"  # the one non-label output token (not a word, not a class)
OFF_LABEL_LOGIT = 2.0  # fixed logit of the off-label token (empty text -> mass ~0.45)
CASE_SPLIT = 0.8  # share of an emotion's probability on the lowercase token; rest capitalised

DEFAULT_LEXICON: dict[str, str] = {
    "angry": "anger", "furious": "anger", "hate": "anger", "mad": "anger",
    "disgusting": "disgust", "gross": "disgust", "nasty": "disgust", "sick": "disgust",
    "scared": "fear", "afraid": "fear", "terrified": "fear", "nervous": "fear",
    "happy": "joy", "love": "joy", "great": "joy", "glad": "joy",
    "sad": "sadness", "miss": "sadness", "cry": "sadness", "lonely": "sadness",
    "wow": "surprise", "shocked": "surprise", "unexpected": "surprise", "surprised": "surprise",
}

DEFAULT_CAPABILITIES = Capabilities(scores=True, gradients=False, generation=False,
                                    repeated_calls=True)

_WORD_RE = re.compile(r"[a-z']+")


def words(text: str) -> list[str]:
    """Lowercased words of a text, as the FakeModel reads them."""
    return _WORD_RE.findall(text.lower())


def _user_text(messages: list[dict]) -> str:
    """Content of the last user message; the system message is ignored."""
    for message in reversed(messages):
        if message.get("role") == "user":
            return message["content"]
    raise ValueError("prompt has no user message")


class FakeModel(ModelComponent):
    """Lexicon-based stand-in for an LLM: prompt in, raw first-token probabilities out.

    logit(emotion) = WORD_WEIGHT x number of lexicon words for that emotion; the off-label
    token has a fixed logit OFF_LABEL_LOGIT; softmax over the 7 logits; each emotion is
    emitted as two casings ("joy" CASE_SPLIT, "Joy" the rest) -> 13 tokens per text.
    """

    model_id = "fake-lexicon-v1"

    def __init__(self, lexicon: Mapping[str, str] = DEFAULT_LEXICON,
                 capabilities: Capabilities | None = None,
                 fail_on: Iterable[str] = frozenset()) -> None:
        unknown = set(lexicon.values()) - set(EMOTIONS)
        if unknown:
            raise ValueError(f"lexicon maps to unknown emotions: {sorted(unknown)}")
        self.lexicon: dict[str, str] = dict(lexicon)
        self.capabilities = capabilities or DEFAULT_CAPABILITIES
        self.fail_on: frozenset[str] = frozenset(fail_on)
        self.n_calls: int = 0  # texts actually scored (failed ones included)

    def score(self, messages_batch: list[list[dict]]) -> list[RawOutput]:
        """Score each prompt's user text; one RawOutput per prompt, same order."""
        texts = [_user_text(messages) for messages in messages_batch]  # raise before scoring
        return [self._score_one(text) for text in texts]

    def _score_one(self, text: str) -> RawOutput:
        start = time.perf_counter()
        self.n_calls += 1
        text_words = words(text)
        if text in self.fail_on:
            return RawOutput((), "complete", time.perf_counter() - start, len(text_words),
                             error="FakeModel: forced failure")
        return RawOutput(self._token_probs(text_words), "complete",
                         time.perf_counter() - start, len(text_words))

    def _token_probs(self, text_words: list[str]) -> tuple[tuple[str, float], ...]:
        counts = Counter(self.lexicon[w] for w in text_words if w in self.lexicon)
        logits = {e: WORD_WEIGHT * counts[e] for e in EMOTIONS}
        logits[OFF_LABEL_TOKEN] = OFF_LABEL_LOGIT
        top = max(logits.values())
        exp = {k: math.exp(v - top) for k, v in logits.items()}
        total = sum(exp.values())
        pairs = [(OFF_LABEL_TOKEN, exp[OFF_LABEL_TOKEN] / total)]
        for e in EMOTIONS:
            p = exp[e] / total
            pairs += [(e, CASE_SPLIT * p), (e.capitalize(), (1 - CASE_SPLIT) * p)]
        return tuple(sorted(pairs, key=lambda tp: (-tp[1], tp[0])))
