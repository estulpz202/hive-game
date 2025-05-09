from hive.behaviors.base import BugBehavior
from hive.board import Board
from hive.models.bug import Bug
from hive.models.position import Position
from hive.rules import RuleEngine

SPIDER_SLIDE = 3  # Number of slides the spider must make

class SpiderBehavior(BugBehavior):
    """Movement rules for the Spider: must slide exactly three spaces without backtracking."""

    def get_valid_moves(self, bug: Bug, board: Board) -> list[Position]:
        """
        Returns valid positions the spider can reach by sliding exactly 3 steps.

        Conditions: Removing spider obeys one hive rule, dest is exactly 3 spaces away,
        dest is unoccupied, dest obeys OHR, and dest obeys FOM.

        Args:
            bug (Bug): The Spider bug.
            board (Board): The game board.

        Returns:
            list[Position]: Valid destinations for the spider.
        """
        # Check one hive rule for removing bug
        if not RuleEngine.is_one_hive_move(board, bug.position):
            return []

        valid = set()

        # Perform recursive DFS to explore all connected valid positions
        def dfs(cur_pos: Position, path: list[Position]):
            # Check sliding exactly 3 steps (depth limit)
            if len(path) == SPIDER_SLIDE:
                valid.add(cur_pos)
                return

            # Check adjacent moves
            for nbor in cur_pos.neighbors():
                # Check move not backtracking, unoccupied, OHR for dest, and FOM
                if (nbor in path or
                    board.is_occupied(nbor) or
                    not RuleEngine.dest_is_connected(board, bug.position, nbor) or
                    not RuleEngine.can_slide_to(board, cur_pos, nbor)):
                    continue

                dfs(nbor, path + [nbor])

        dfs(bug.position, [])

        return list(valid)
