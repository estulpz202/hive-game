from hive.behaviors.base import BugBehavior
from hive.board import Board
from hive.models.bug import Bug
from hive.models.position import Position
from hive.rules import RuleEngine


class AntBehavior(BugBehavior):
    """Movement rules for the Ant: slide to any reachable position around the hive."""

    def get_valid_moves(self, bug: Bug, board: Board) -> list[Position]:
        """
        Returns all reachable positions the ant can legally slide to.

        Conditions: Removing ant obeys one hive rule, dest is connected,
        dest is unoccupied, dest obeys OHR, and dest obeys FOM.

        Args:
            bug (Bug): The Ant attempting to move.
            board (Board): The current game board.

        Returns:
            list[Position]: Valid destinations for the ant.
        """
        # Check one hive rule for removing bug
        if not RuleEngine.is_one_hive_move(board, bug.position):
            return []

        visited = set()
        stack = [bug.position]
        valid = set()

        # Perform DFS to explore all connected valid positions
        while stack:
            cur_pos = stack.pop()
            # Check adjacent destinations
            for dest in cur_pos.neighbors():
                if dest in visited:
                    continue
                visited.add(dest)

                # Check dest unoccupied, OHR for dest, and FOM
                if (board.is_occupied(dest) or
                    not RuleEngine.dest_is_connected(board, bug.position, dest) or
                    not RuleEngine.can_slide_to(board, cur_pos, dest)):
                    continue

                valid.add(dest)
                stack.append(dest)

        return list(valid)
