class Player:
    """Represents a player in the Hive game."""

    def __init__(self, color: str):
        self.color = color
        self.reserve = []  # List of BugType not yet placed
        self.placed_bugs = []  # List of Bug instances placed on the board

    def has_placed_queen(self) -> bool:
        """Return True if the Queen Bee has been placed."""
        return any(b.bug_type.name == "QUEEN_BEE" for b in self.placed_bugs)
