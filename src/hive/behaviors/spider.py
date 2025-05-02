from hive.behaviors.base import BugBehavior


class SpiderBehavior(BugBehavior):
    """Movement rules for spider piece."""

    def get_valid_moves(self, bug, board):
        """Return valid positions."""
        return []
