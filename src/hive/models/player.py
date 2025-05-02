from hive.models.bug import BugType


class Player:
    """
    Represents a Hive player.

    Tracks bug reserve (unplaced bugs) and placed bugs on the board.
    """

    def __init__(self, color: str):
        self.color = color.upper()
        self.reserve: list[BugType] = (
            [BugType.QUEEN_BEE]
            + [BugType.ANT] * 3
            + [BugType.BEETLE] * 2
            + [BugType.SPIDER] * 2
            + [BugType.GRASSHOPPER] * 3
        )
        self.placed: list = []

    def has_placed_queen(self) -> bool:
        """Return True if the Queen Bee has been placed on the board."""
        return any(bug.bug_type == BugType.QUEEN_BEE for bug in self.placed)

    def remove_from_reserve(self, bug_type: BugType) -> bool:
        """
        Removes a bug of the given type from reserve if available.

        Returns:
            bool: True if removed successfully, False if not available.
        """
        if bug_type in self.reserve:
            self.reserve.remove(bug_type)
            return True
        return False

    def add_to_placed(self, bug) -> None:
        """
        Adds a bug to the placed list.

        Args:
            bug: The bug to be added.
        """
        self.placed.append(bug)