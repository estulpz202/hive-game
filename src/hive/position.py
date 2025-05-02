# src/hive/position.py
from dataclasses import dataclass

@dataclass(frozen=True)
class Position:
    """
    Represents a position on a hexagonal grid using axial coordinates (q, r).
    """
    q: int  # axial coordinate q
    r: int  # axial coordinate r

    def neighbors(self):
        """
        Calculate and return the 6 adjacent positions (neighbors) on the hexagonal grid.

        Returns:
            list[Position]: A list of 6 Position objects representing the neighboring hexes.
        """
        directions = [
            (1, 0), (1, -1), (0, -1),
            (-1, 0), (-1, 1), (0, 1)
        ]
        return [Position(self.q + dq, self.r + dr) for dq, dr in directions]

    def __hash__(self):
        """
        Generate a hash value for the Position object.

        Returns:
            int: The hash value based on the (q, r) coordinates.
        """
        return hash((self.q, self.r))

    def __eq__(self, other):
        """
        Check equality between this Position and another object.

        Args:
            other (object): The object to compare against.

        Returns:
            bool: True if the other object is a Position with the same (q, r) coordinates, False otherwise.
        """
        if not isinstance(other, Position):
            return NotImplemented
        return self.q == other.q and self.r == other.r