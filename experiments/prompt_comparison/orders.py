"""Label orders for the position-bias check: the 6 cyclic rotations of EMOTIONS."""
from data.schema import EMOTIONS

ORDERS: dict[str, list[str]] = {
    f"O{k + 1}": EMOTIONS[k:] + EMOTIONS[:k] for k in range(len(EMOTIONS))
}  # O1 = EMOTIONS (canonical); each emotion sits in each position exactly once
