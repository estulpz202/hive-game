from hive.behaviors.base import BugBehavior
from hive.board import Board
from hive.models.bug import Bug
from hive.models.position import Position


class QueenBehavior(BugBehavior):
    """Movement rules for the Queen Bee: slide to one adjacent free tile."""

    def get_valid_moves(self, bug: Bug, board: Board) -> list[Position]:
        """
        Returns valid adjacent positions the queen can slide into.

        Conditions: Removing bug obeys one hive rule, adjacent dest,
        dest is unoccupied, dest obeys OHR, and dest obeys FOM.

        Args:
            bug (Bug): The Queen Bee bug.
            board (Board): The game board.

        Returns:
            list[Position]: Legal move destinations for the queen.
        """
        valid = []

        # Check one hive rule for removing bug
        if not board.is_one_hive_move(bug.position):
            return valid
        
        # Temporarily remove bug
        removed_bug = board.remove_top_bug(bug.position)

        # Check adjacent destinations
        for dest in bug.position.neighbors():
            # Check dest unoccupied, OHR for dest, and FOM
            if board.is_occupied(dest):
                continue
            if not any(board.is_occupied(nbor) for nbor in dest.neighbors()):
                continue
            if board.can_slide_to(bug.position, dest):
                valid.append(dest)

        # Restore the removed bug
        board._grid[bug.position].append(removed_bug)

        return valid
