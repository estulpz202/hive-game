from dataclasses import dataclass
from functools import cache


# The @dataclass decorator generates special methods like __init__ and __eq__.
# The frozen=True parameter makes the dataclass immutable.
@dataclass(frozen=True)
class Position:
    """Position on a hexagonal grid using axial coordinates (q, r)."""

    q: int  # axial coordinate q
    r: int  # axial coordinate r

    # @cache stores the result of this method to avoid recalculating neighbors.
    @cache
    def neighbors(self) -> list["Position"]:
        """Calculate and return the 6 adjacent positions (neighbors) on the hex grid."""
        directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
        return [Position(self.q + dq, self.r + dr) for dq, dr in directions]
