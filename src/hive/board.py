from collections import defaultdict
from collections.abc import Iterator

from hive.models.bug import Bug
from hive.models.player import Player
from hive.models.position import Position

MAX_SLIDE_BLOCKERS = 1  # Max number of blocking neighbors to allow sliding

class Board:
    """
    Represents the Hive game board.

    Maintains bug positions, including stacked bugs (e.g., beetles),
    and provides utility methods for interacting with the board state.
    """

    def __init__(self):
        # Using defaultdict to automatically initialize empty lists for positions
        self._grid: dict[Position, list[Bug]] = defaultdict(list)

    def place_bug(self, bug: Bug, position: Position) -> None:
        """Places a bug on the board at the given position."""
        bug.position = position
        bug.on_top = len(self._grid[position])
        self._grid[position].append(bug)

    def remove_top_bug(self, position: Position) -> Bug | None:
        """Removes and returns the top bug at a given position."""
        stack = self._grid.get(position)
        if stack:
            return stack.pop()
        return None

    def get_stack(self, position: Position) -> list[Bug]:
        """Returns the bug stack at a given position."""
        return self._grid.get(position, [])

    def get_top_bug(self, position: Position) -> Bug | None:
        """Returns the top bug at a position, or None if empty."""
        stack = self._grid.get(position, [])
        return stack[-1] if stack else None

    def get_bug_at(self, position: Position) -> Bug | None:
        """Alias for get_top_bug — returns the bug on top at a position."""
        return self.get_top_bug(position)

    def get_all_bugs(self) -> list[Bug]:
        """Returns a flat list of all bugs on the board."""
        return [bug for stack in self._grid.values() for bug in stack]

    def is_occupied(self, position: Position) -> bool:
        """Returns True if there is at least one bug at the position."""
        return bool(self._grid.get(position))

    def occupied_positions(self) -> Iterator[Position]:
        """Returns all positions that have at least one bug."""
        return (pos for pos, stack in self._grid.items() if stack)

    def can_place_bug(self, player: Player, position: Position) -> bool:
        """
        Checks whether a bug can be placed at the given position.

        Conditions: The tile is empty, bug must touch at least one of their own bugs,
        bug may not touch opponent's bugs. Note, a stack takes the color of the bug on top.

        Exceptions: The first bug placed will not touch anything, and
        the second bug placed will touch the first bug of the opponent.

        Args:
            player (Player): The player attempting to place the bug.
            position (Position): The position where the bug is to be placed.

        Returns:
            bool: True if the bug can be legally placed, False otherwise.
        """
        if self.is_occupied(position):
            return False

        # First bug placed: allow isolated placement
        # Checks if board is fully unoccupied
        if not any(self.occupied_positions()):
            return True

        # Get the top bug from each occupied neighboring position
        neighbor_bugs = [
            self.get_top_bug(nbor)
            for nbor in position.neighbors() if self.is_occupied(nbor)
        ]

        # Second bug placed: must touch the opponent's first bug
        # Return checks if at least one neighboring bug belongs to the opponent
        if len(list(self.occupied_positions())) == 1:
            return any(b.owner != player for b in neighbor_bugs if b is not None)

        if not neighbor_bugs:
            return False

        # Checks if all neighboring bugs belong to the same player
        return all(b.owner == player for b in neighbor_bugs if b is not None)

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

        # Temporarily remove top bug
        removed_bug = self.remove_top_bug(from_pos)

        # If to_pos provided and has no occupied neighbors, moved bug will be unconnected
        if to_pos and not any(self.is_occupied(nbor) for nbor in to_pos.neighbors()):
            self._grid[from_pos].append(removed_bug)
            return False

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

    def can_move_bug(self, bug: Bug, to_pos: Position) -> bool:
        """
        Determines if the given bug can legally move to the specified position.

        Checks: Dest is different from cur position, bug is on top of its stack,
        hive remains connected during move, and bug specific logic & FOM allows it.

        Args:
            bug (Bug): The bug attempting to move.
            to_pos (Position): The target position for the bug.

        Returns:
            bool: True if the bug can legally move to the target position, False otherwise.
        """
        from hive.behaviors import get_behavior_for  # Lazy import to avoid circular dependency

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
        behavior = get_behavior_for(bug.bug_type)
        if to_pos not in behavior.get_valid_moves(bug, self):
            return False

        return True

    def move_bug(self, bug: Bug, to_pos: Position) -> bool:
        """
        Moves a bug to a new position if the move is legal.

        Args:
            bug (Bug): The bug to move.
            to_pos (Position): The target position for the bug.

        Returns:
            bool: True if the bug was moved successfully, False otherwise.
        """
        if not self.can_move_bug(bug, to_pos):
            return False

        self.remove_top_bug(bug.position)
        self.place_bug(bug, to_pos)
        return True
