from dataclasses import dataclass

# The @dataclass decorator generates special methods like __init__ and __eq__.
# The frozen=True parameter makes the dataclass immutable.
@dataclass(frozen=True)
class Position:
    """Position on a hexagonal grid using axial coordinates (q, r)."""
    q: int  # axial coordinate q
    r: int  # axial coordinate r

    def neighbors(self):
        """
        Calculate and return the 6 adjacent positions (neighbors) on the hex grid.

        Returns:
            list[Position]: A list of 6 Position objects representing the neighboring hexes.
        """
        directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
        return [Position(self.q + dq, self.r + dr) for dq, dr in directions]
