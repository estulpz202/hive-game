from hive.models.bug import Bug
from hive.models.player import Player
from hive.models.position import Position

NUM_BLOCKERS_FOM = 2  # The number of blocking neighbors to restrict sliding

class RuleEngine:
    """Encapsulates Hive rule enforcement for placement and movement validation."""

    @staticmethod
    def get_all_valid_places(board, player: Player) -> set[Position]:
        """
        Returns a set of legal positions where the player can place any bug from reserve.

        Args:
            board: The current board state.
            player (Player): The player attempting to place the bug.

        Returns:
            set[Position]: Legal placement tiles based on placement rules.
        """
        occupied = list(board.occupied_positions())

        # First bug placed (board unoccupied)
        # Allow isolated placement at (0, 0)
        if not occupied:
            return {Position(0, 0)}

        # Second bug placed (one occupied pos and stack height is 1)
        # Must touch the opponent's first bug
        if len(occupied) == 1:
            only_pos = occupied[0]
            if len(board.get_stack(only_pos)) == 1:
                return set(only_pos.neighbors())

        # Normal case: Must touch own bug(s) only
        positions = set()
        seen = set()
        for bug in player.placed:
            if not RuleEngine.is_on_top(board, bug):
                continue

            for pos in bug.position.neighbors():
                if board.is_occupied(pos) or pos in seen:
                    continue
                seen.add(pos)
                nbor_bugs = [board.get_top_bug(n) for n in pos.neighbors() if board.is_occupied(n)]

                if nbor_bugs and all(b.owner == player for b in nbor_bugs if b is not None):
                    positions.add(pos)

        return positions

    @staticmethod
    def is_on_top(board, bug: Bug) -> bool:
        """Returns True if the given bug is on top of its stack."""
        return board.get_top_bug(bug.position) == bug

    @staticmethod
    def can_place_bug(board, player: Player, pos: Position,
                      valid_places: set[Position] | None = None) -> bool:
        """
        Checks whether a bug can be placed at the given position.

        Conditions: The tile is empty, bug must touch only their own bugs,
        with exceptions at the start. Note, a stack takes the color of the bug on top.

        Args:
            board: The current board state.
            player (Player): The player attempting to place the bug.
            pos (Position): The position where the bug is to be placed.
            valid_places (set[Position] | None): Optional precomputed legal positions.

        Returns:
            bool: True if the bug can be legally placed, False otherwise.
        """
        if valid_places is not None:
            return pos in valid_places

        if board.is_occupied(pos):
            return False

        occupied = list(board.occupied_positions())

        # First bug placed (board unoccupied)
        # Allow isolated placement at (0, 0)
        if not occupied:
            return Position(0, 0) == pos

        # Second bug placed (one occupied pos and stack height is 1)
        # Must touch the opponent's first bug
        if len(occupied) == 1 and len(board.get_stack(occupied[0])) == 1:
            return pos in occupied[0].neighbors()

        # Normal case: Must touch own bug(s) only
        # Get the top bug from each occupied neighboring position
        nbor_bugs = [board.get_top_bug(n) for n in pos.neighbors() if board.is_occupied(n)]
        if not nbor_bugs:
            return False

         # Check if all neighboring bugs belong to player
        return all(b.owner == player for b in nbor_bugs if b is not None)

    @staticmethod
    def is_one_hive_move(board, from_pos: Position, to_pos: Position = None) -> bool:
        """
        Checks if hive stays connected when moving top bug at from_pos (to to_pos).

        Args:
            board: The current board state.
            from_pos (Position): The position to remove the bug from.
            to_pos (Position): The position to move the bug to (optional).

        Returns:
            bool: True if the hive stays connected, False otherwise.
        """
        if not board.is_occupied(from_pos):
            return True

        if to_pos and not RuleEngine.dest_is_connected(board, from_pos, to_pos):
            return False

        # Temporarily remove top bug
        # If from_pos still occupied, the hive remains connected
        removed_bug = board._remove_top_bug(from_pos)
        if board.is_occupied(from_pos):
            board._drop_bug(removed_bug, from_pos)
            return True

        # Otherwise, check if remaining occupied positions are connected
        remaining = set(board.occupied_positions())
        if not remaining:
            board._drop_bug(removed_bug, from_pos)
            return True

        # Start DFS from any remaining position
        visited = set()
        stack = [next(iter(remaining))]
        while stack:
            cur_pos = stack.pop()
            if cur_pos in visited:
                continue
            visited.add(cur_pos)
            for nbor in cur_pos.neighbors():
                if nbor in remaining:
                    stack.append(nbor)

        # Restore the removed bug
        board._drop_bug(removed_bug, from_pos)

        # Check if all remaining positions were visited
        return visited == remaining

    @staticmethod
    def dest_is_connected(board, from_pos: Position, to_pos: Position) -> bool:
        """Checks if the destination will remain connected to the hive after moving."""
        # If destination is already part of the hive (occupied), it's connected
        if board.is_occupied(to_pos):
            return True

        # Else if: from_pos stays occupied, safe to just check neighbors of to_pos
        if len(board.get_stack(from_pos)) > 1:
            return any(board.is_occupied(nbor) for nbor in to_pos.neighbors())

        # Else: skip from_pos when checking neighbors
        for nbor in to_pos.neighbors():
            if nbor == from_pos:
                continue
            if board.is_occupied(nbor):
                return True

        return False

    @staticmethod
    def can_slide_to(board, from_pos: Position, to_pos: Position) -> bool:
        """
        Determines if a bug can slide between two adjacent positions.

        Conditions: Both positions must be adjacent and follow FOM rule.

        Args:
            board: The current board state.
            from_pos (Position): The bug's current position.
            to_pos (Position): The position the bug wants to slide into.

        Returns:
            bool: True if the bug can legally slide to the destination, False otherwise.
        """
        if to_pos not in from_pos.neighbors():
            return False

        shared_neighbors = set(from_pos.neighbors()) & set(to_pos.neighbors())
        blocked_sides = sum(1 for nbor in shared_neighbors if board.is_occupied(nbor))

        return blocked_sides < NUM_BLOCKERS_FOM

    @staticmethod
    def can_climb_to(board, from_pos: Position, to_pos: Position) -> bool:
        """
        Determines if a bug can legally climb between two adjacent stacks.

        Conditions: Both positions must be adjacent and follows FOM rule,
        uses can_slide if same level, otherwise checks if both neighbors taller.

        Args:
            board: The current board state.
            from_pos (Position): Current position of the beetle.
            to_pos (Position): Target adjacent position.

        Returns:
            bool: True if climbing is allowed, False otherwise.
        """
        if to_pos not in from_pos.neighbors():
            return False

        from_height = len(board.get_stack(from_pos)) - 1
        to_height = len(board.get_stack(to_pos))

        if from_height == to_height:
            return RuleEngine.can_slide_to(board, from_pos, to_pos)

        shared_neighbors = set(from_pos.neighbors()) & set(to_pos.neighbors())

        taller_blockers = sum(
            1 for nbor in shared_neighbors
            if len(board.get_stack(nbor)) > from_height and len(board.get_stack(nbor)) > to_height
        )

        return taller_blockers < NUM_BLOCKERS_FOM

    @staticmethod
    def get_valid_moves(board, player: Player) -> dict[Bug, list[Position]]:
        """
        Returns a dictionary of player's movable bugs and their legal destination positions.

        Args:
            board: The current board state.
            player (Player): The current player.

        Returns:
            dict[Bug, list[Position]]: Map from bug to valid move positions.
        """
        if not player.has_placed_queen:
            return {}

        moves = {}
        for bug in player.placed:
            if not RuleEngine.is_on_top(board, bug):
                continue

            valid = bug.get_valid_moves(board)
            if valid:
                moves[bug] = valid

        return moves

    @staticmethod
    def can_move_bug(board, bug: Bug, to_pos: Position,
                     valid_moves: dict[Bug, list[Position]] | None = None) -> bool:
        """
        Determines if the given bug can legally move to the specified position.

        Checks: Destination is different from current position, bug is on top of its stack,
        and bug specific logic, OHR, FOM allows it.

        Args:
            board: The current board state.
            bug (Bug): The bug attempting to move.
            to_pos (Position): The target position for the bug.
            valid_moves (dict[Bug, list[Position]] | None): Optional precomputed valid moves.

        Returns:
            bool: True if the bug can legally move to the target position, False otherwise.
        """
        if valid_moves is not None:
            return to_pos in valid_moves.get(bug, [])

        if bug.position == to_pos:
            return False

        if not RuleEngine.is_on_top(board, bug):
            return False

        # Check bug specific movement rules, OHR, and FOM
        return to_pos in bug.get_valid_moves(board)
