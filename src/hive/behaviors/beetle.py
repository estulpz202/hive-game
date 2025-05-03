from hive.behaviors.base import BugBehavior


class BeetleBehavior(BugBehavior):
    """Movement rules for beetle piece."""

    def get_valid_moves(self, bug, board):
        """Return valid positions."""
        return []
