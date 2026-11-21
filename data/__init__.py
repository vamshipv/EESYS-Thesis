"""Data and Input Module: GoEmotions loading, filtering, fixed samples."""
from data.loader import load_samples
from data.schema import EMOTIONS, Sample

__all__ = ["EMOTIONS", "Sample", "load_samples"]
