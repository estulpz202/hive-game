from hive.behaviors.base import BugBehavior


class AntBehavior(BugBehavior):
    """Movement rules for ant piece."""

    def get_valid_moves(self, bug, board):
        """Return valid positions."""
        return []
