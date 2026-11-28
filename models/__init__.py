"""Model Components: raw model access behind one shared contract (`base.py`)."""
from models.base import Capabilities, ModelComponent, RawOutput
from models.fake_model import FakeModel

__all__ = ["Capabilities", "FakeModel", "ModelComponent", "RawOutput"]
