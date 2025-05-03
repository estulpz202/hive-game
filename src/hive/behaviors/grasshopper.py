from hive.behaviors.base import BugBehavior


class GrasshopperBehavior(BugBehavior):
    """Movement rules for grasshopper piece."""

    def get_valid_moves(self, bug, board):
        """Return valid positions."""
        return []
