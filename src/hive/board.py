from collections import defaultdict
from collections.abc import Iterator

from hive.models.bug import Bug
from hive.models.player import Player
from hive.models.position import Position

NUM_BLOCKERS_FOM = 2  # The number of blocking neighbors to restrict sliding

class Board:
    """
    Represents the Hive game board.

    Maintains bug positions, including stacked bugs (e.g., beetles),
    and provides utility methods for interacting with the board state.
    """

    def __init__(self):
        # Using defaultdict to automatically initialize empty lists for positions
        self._grid: dict[Position, list[Bug]] = defaultdict(list)

    def remove_top_bug(self, position: Position) -> Bug | None:
        """Removes and returns the top bug at a given position."""
        stack = self._grid.get(position)
        if stack:
            return stack.pop()
        return None

    def _drop_bug(self, bug: Bug, position: Position) -> None:
        """Unconditionally places a bug on the stack at the given position."""
        bug.position = position
        bug.height = len(self._grid[position])
        self._grid[position].append(bug)

        # Update the player's reserve and placed bugs
        player = bug.owner
        player.remove_from_reserve(bug.bug_type)
        player.add_to_placed(bug)

    def get_stack(self, position: Position) -> list[Bug]:
        """Returns the bug stack at a given position."""
        return self._grid.get(position, [])

    def get_top_bug(self, position: Position) -> Bug | None:
        """Returns the top bug at a position, or None if empty."""
        stack = self._grid.get(position, [])
        return stack[-1] if stack else None

    def get_all_bugs(self) -> list[Bug]:
        """Returns a flat list of all bugs on the board."""
        return [bug for stack in self._grid.values() for bug in stack]

    def is_occupied(self, position: Position) -> bool:
        """Returns True if there is at least one bug at the position."""
        return bool(self._grid.get(position))

    def occupied_positions(self) -> Iterator[Position]:
        """Returns all positions that have at least one bug."""
        return (pos for pos, stack in self._grid.items() if stack)

    def get_all_valid_positions(self, player: Player) -> set[Position]:
        """
        Returns a set of legal positions where the player can place any bug from reserve.

        Args:
            player (Player): The player attempting to place the bug.

        Returns:
            set[Position]: Legal placement tiles based on placement rules.
        """
        occupied = list(self.occupied_positions())

        # First bug placed (board unoccupied)
        # Allow isolated placement at (0, 0)
        if not occupied:
            return {Position(0, 0)}

        # Second bug placed (one occupied pos and stack height is 1)
        # Must touch the opponent's first bug
        if len(occupied) == 1:
            only_pos = occupied[0]
            if len(self.get_stack(only_pos)) == 1:
                return set(only_pos.neighbors())

        # Normal case: Must touch own bug(s) only
        positions = set()
        seen = set()
        for bug in player.placed:
            # bug must be on top of the stack
            if bug.height != len(self.get_stack(bug.position)) - 1:
                continue

            for pos in bug.position.neighbors():
                # Skip if occupied or already seen
                if self.is_occupied(pos) or pos in seen:
                    continue
                seen.add(pos)
                # Get the top bug from each occupied neighboring position
                nbor_bugs = [self.get_top_bug(n) for n in pos.neighbors() if self.is_occupied(n)]

                # Must have neighbors, and all of them must belong to the player
                if nbor_bugs and all(b.owner == player for b in nbor_bugs if b is not None):
                    positions.add(pos)

        return positions

    def can_place_bug(self, player: Player, pos: Position,
                      valid_positions: set[Position] | None = None) -> bool:
        """
        Checks whether a bug can be placed at the given position.

        Conditions: The tile is empty, bug must touch only their own bugs,
        some exceptions at start. Note, a stack takes the color of the bug on top.

        Args:
            player (Player): The player attempting to place the bug.
            pos (Position): The position where the bug is to be placed.
            valid_positions (set[Position] | None): Optional precomputed legal positions.

        Returns:
            bool: True if the bug can be legally placed, False otherwise.
        """
        if valid_positions is not None:
            return pos in valid_positions

        if self.is_occupied(pos):
            return False

        occupied = list(self.occupied_positions())

        # First bug placed (board unoccupied)
        # Allow isolated placement at (0, 0)
        if not occupied:
            return Position(0, 0) == pos

        # Second bug placed (one occupied pos and stack height is 1)
        # Must touch the opponent's first bug
        if len(occupied) == 1 and len(self.get_stack(occupied[0])) == 1:
            return pos in occupied[0].neighbors()

        # Normal case: Must touch own bug(s) only
        # Get the top bug from each occupied neighboring position
        nbor_bugs = [self.get_top_bug(n) for n in pos.neighbors() if self.is_occupied(n)]

        # Must have at least one neighbor
        if not nbor_bugs:
            return False

        # Check if all neighboring bugs belong to player
        return all(b.owner == player for b in nbor_bugs if b is not None)

    def place_bug(self, bug: Bug, pos: Position,
                  valid_positions: set[Position] | None = None) -> bool:
        """
        Attempts to place a bug at a given position on the board.

        Args:
            bug (Bug): The bug to place.
            pos (Position): The target position to place the bug.
            valid_positions (set[Position] | None): Optional precomputed legal positions.

        Returns:
            bool: True if the bug was successfully placed, False otherwise.
        """
        if not self.can_place_bug(bug.owner, pos, valid_positions):
            return False

        self._drop_bug(bug, pos)
        return True

    def dest_is_connected(self, from_pos: Position, to_pos: Position) -> bool:
        """Checks if the destination will remain connected to the hive after moving."""
        # If destination is already part of the hive (occupied), it's connected
        if self.is_occupied(to_pos):
            return True

        # Else if: from_pos stays occupied, safe to just check neighbors of to_pos
        if len(self.get_stack(from_pos)) > 1:
            return any(self.is_occupied(nbor) for nbor in to_pos.neighbors())

        # Else: skip from_pos when checking neighbors
        for nbor in to_pos.neighbors():
            if nbor == from_pos:
                continue
            if self.is_occupied(nbor):
                return True

        return False

    def is_one_hive_move(self, from_pos: Position, to_pos: Position = None) -> bool:
        """
        Checks if hive stays connected when moving top bug at from_pos (to to_pos).

        Args:
            from_pos (Position): The position to remove the bug from.
            to_pos (Position): The position to move the bug to (optional).

        Returns:
            bool: True if the hive stays connected, False otherwise.
        """
        # If nothing to remove, hive is unchanged
        if not self.is_occupied(from_pos):
            return True

        # If to_pos provided and has no occupied neighbors, moved bug will be unconnected
        if to_pos and not self.dest_is_connected(from_pos, to_pos):
            return False

        # Temporarily remove top bug
        removed_bug = self.remove_top_bug(from_pos)

        # If from_pos still occupied, the hive remains connected
        if self.is_occupied(from_pos):
            self._grid[from_pos].append(removed_bug)
            return True

        # Otherwise, check if remaining occupied positions are connected
        remaining = set(self.occupied_positions())
        # If no bugs remain, the hive is trivially connected
        if not remaining:
            self._grid[from_pos].append(removed_bug)
            return True

        # Start DFS from any remaining position
        # Use next(iter()) to get an arbitrary position from the remaining set
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
        self._grid[from_pos].append(removed_bug)

        # Check if all remaining positions were visited
        return visited == remaining

    def can_slide_to(self, from_pos: Position, to_pos: Position) -> bool:
        """
        Determines if a bug can slide between two adjacent positions.

        Conditions: Both positions must be adjacent and follows FOM rule.

        Args:
            from_pos (Position): The bug's current position.
            to_pos (Position): The position the bug wants to slide into.

        Returns:
            bool: True if the bug can legally slide to the destination, False otherwise.
        """
        if to_pos not in from_pos.neighbors():
            return False

        # Get the positions that are neighbors of both from and to
        shared_neighbors = set(from_pos.neighbors()) & set(to_pos.neighbors())
        # Count how many of those are occupied
        blocked_sides = sum(1 for nbor in shared_neighbors if self.is_occupied(nbor))

        # Bug can slide if fewer than 2 adjacent tiles block the gap
        return blocked_sides < NUM_BLOCKERS_FOM

    def can_climb_to(self, from_pos: Position, to_pos: Position) -> bool:
        """
        Determines if a bug can legally climb between two adjacent stacks.

        Conditions: Both positions must be adjacent and follows FOM rule,
        uses can_slide if same level, otherwise checks if both neighbors taller.

        Args:
            from_pos (Position): Current position of the beetle.
            to_pos (Position): Target adjacent position.

        Returns:
            bool: True if climbing is allowed, False otherwise.
        """
        if to_pos not in from_pos.neighbors():
            return False

        # Subtract 1 since bug is being moved, so doesn't count towards height
        from_height = len(self.get_stack(from_pos)) - 1
        to_height = len(self.get_stack(to_pos))

        # If heights are equal, treat as a slide (must obey slide FOM)
        if from_height == to_height:
            return self.can_slide_to(from_pos, to_pos)

        # Get neighbors shared by both from and to positions
        shared_neighbors = set(from_pos.neighbors()) & set(to_pos.neighbors())

        # Count shared neighbors that are taller than both from and to stacks
        taller_blockers = sum(
            1 for nbor in shared_neighbors
            if len(self.get_stack(nbor)) > from_height and len(self.get_stack(nbor)) > to_height
        )

        # Buc can climb is allowed if fewer than 2 taller blockers exist
        return taller_blockers < NUM_BLOCKERS_FOM

    def get_all_valid_moves(self, player: Player) -> dict[Bug, list[Position]]:
        """
        Returns a dictionary of player's movable bugs and their legal destination positions.

        Args:
            player (Player): The current player.

        Returns:
            dict[Bug, list[Position]]: Map from bug to valid move positions.
        """
        # Check if the player has placed their queen
        if not player.has_placed_queen:
            return {}

        from hive.behaviors import get_behavior_for  # Lazy import, avoid circularity
        moves = {}
        for bug in player.placed:
            # Skip if bug not on top
            if self.get_top_bug(bug.position) != bug:
                continue

            behavior = get_behavior_for(bug.bug_type)
            valid = behavior.get_valid_moves(bug, self)
            if valid:
                moves[bug] = valid

        return moves

    def can_move_bug(self, bug: Bug, to_pos: Position,
                     valid_moves: dict[Bug, list[Position]] | None = None) -> bool:
        """
        Determines if the given bug can legally move to the specified position.

        Checks: Dest is different from cur position, bug is on top of its stack,
        hive remains connected during move, and bug specific logic & FOM allows it.

        Args:
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

        # Check bug is on top of its stack
        stack = self.get_stack(bug.position)
        if not stack or stack[-1] != bug:
            return False

        # Check one hive rule
        if not self.is_one_hive_move(bug.position, to_pos):
            return False

        # Check bug specific movement rules and FOM via behavior strategy
        from hive.behaviors import get_behavior_for  # Lazy import, avoid circularity
        behavior = get_behavior_for(bug.bug_type)
        if to_pos not in behavior.get_valid_moves(bug, self):
            return False

        return True

    def move_bug(self, bug: Bug, to_pos: Position,
                 valid_moves: dict[Bug, list[Position]] | None = None) -> bool:
        """
        Moves a bug to a new position if the move is legal.

        Args:
            bug (Bug): The bug to move.
            to_pos (Position): The target position for the bug.
            valid_moves (dict[Bug, list[Position]] | None): Optional precomputed valid moves.

        Returns:
            bool: True if the bug was moved successfully, False otherwise.
        """
        if not self.can_move_bug(bug, to_pos, valid_moves):
            return False

        self.remove_top_bug(bug.position)
        self._drop_bug(bug, to_pos)
        return True
