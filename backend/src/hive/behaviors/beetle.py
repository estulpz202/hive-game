from hive.behaviors.base import BugBehavior
from hive.board import Board
from hive.models.bug import Bug
from hive.models.position import Position
from hive.rules import RuleEngine


class BeetleBehavior(BugBehavior):
    """Movement rules for the Beetle: may slide or climb onto adjacent bugs."""

    def get_valid_moves(self, bug: Bug, board: Board) -> list[Position]:
        """
        Returns valid adjacent positions the beetle can slide or climb to.

        Conditions: Removing beetle obeys OHR, dest obeys OHR, dest obeys FOM.
        slide when staying on the same level, climb up or down a stack of bugs.

        Blocked by FOM: Only if both shared neighbors are taller than both source and dest.

        Args:
            bug (Bug): The beetle attempting to move.
            board (Board): The game board.

        Returns:
            list[Position]: Valid destinations for the beetle.
        """
        # Check one hive rule for removing bug
        if not RuleEngine.is_one_hive_move(board, bug.position):
            return []

        valid = []

        # Check adjacent destinations
        for dest in bug.position.neighbors():
            # Check OHR for dest and FOM
            if (not RuleEngine.dest_is_connected(board, bug.position, dest) or
                not RuleEngine.can_climb_to(board, bug.position, dest)):
                continue

            valid.append(dest)

        return valid
