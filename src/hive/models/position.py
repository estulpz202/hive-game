from dataclasses import dataclass
from functools import cache


# @cache stores the result of this method to avoid recalculating neighbors.
@cache
def get_neighbors(q: int, r: int) -> list["Position"]:
    """Compute adjacent positions (neighbors) using axial coordinate."""
    directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
    return [Position(q + dq, r + dr) for dq, dr in directions]

# The @dataclass decorator generates special methods like __init__ and __eq__.
# The frozen=True parameter makes the dataclass immutable.
@dataclass(frozen=True)
class Position:
    """Position on a hexagonal grid using axial coordinates (q, r)."""

    q: int  # axial coordinate q
    r: int  # axial coordinate r

    def neighbors(self) -> list["Position"]:
        """Get the 6 neighbor positions on the hex grid."""
        return get_neighbors(self.q, self.r)
