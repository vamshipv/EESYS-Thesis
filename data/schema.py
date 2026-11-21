"""Shared data types for the pipeline."""
from dataclasses import dataclass

# Fixed order, used everywhere (probability vectors, matrices, reports).
EMOTIONS: list[str] = ["anger", "disgust", "fear", "joy", "sadness", "surprise"]


@dataclass(frozen=True)
class Sample:
    """One GoEmotions text with its single ground-truth label."""

    id: str
    text: str
    label: str
