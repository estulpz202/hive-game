from hive.models.bugtype import BugType


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
        self.has_placed_queen: bool = False
        self.queen_bug = None

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
        """Adds a bug to the placed list."""
        self.placed.append(bug)
        if not self.has_placed_queen and bug.bug_type == BugType.QUEEN_BEE:
            self.has_placed_queen = True
            self.queen_bug = bug
