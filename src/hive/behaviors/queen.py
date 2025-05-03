from hive.behaviors.base import BugBehavior
from hive.board import Board
from hive.models.bug import Bug
from hive.models.position import Position


class QueenBehavior(BugBehavior):
    """Movement rules for the Queen Bee: slide to one adjacent free tile."""

    def get_valid_moves(self, bug: Bug, board: Board) -> list[Position]:
        """
        Returns valid adjacent positions the qeen can slide into.

        Conditions: Removing queen obeys one hive rule, dest is adjacent,
        dest is unoccupied, dest obeys OHR, and dest obeys FOM.

        Args:
            bug (Bug): The Queen Bee bug.
            board (Board): The game board.

        Returns:
            list[Position]: Valid destinations for the queen.
        """
        # Check one hive rule for removing bug
        if not board.is_one_hive_move(bug.position):
            return []

        valid = []

        # Check adjacent destinations
        for dest in bug.position.neighbors():
            # Check dest unoccupied, OHR for dest, and FOM
            if (board.is_occupied(dest) or
                not board.dest_is_connected(bug.position, dest) or
                not board.can_slide_to(bug.position, dest)):
                continue

            valid.append(dest)

        return valid
