class BugBehavior:
    """Base class for bug movement behavior using the Strategy pattern."""

    def get_valid_moves(self, bug, board):
        """Return a list of valid positions this bug can move to."""
        raise NotImplementedError("Must be implemented by subclass.")
