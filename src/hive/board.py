from collections import defaultdict
from collections.abc import Iterator

from hive.models.bug import Bug
from hive.models.player import Player
from hive.models.position import Position


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

    def get_stack(self, position: Position) -> list[Bug]:
        """Returns the bug stack at a given position."""
        return self._grid.get(position, [])

    def get_top_bug(self, position: Position) -> Bug | None:
        """Returns the top bug at a position, or None if empty."""
        stack = self._grid.get(position, [])
        return stack[-1] if stack else None

    def occupied_positions(self) -> Iterator[Position]:
        """Returns all positions that have at least one bug."""
        return (pos for pos, stack in self._grid.items() if stack)

    def is_occupied(self, position: Position) -> bool:
        """Returns True if there is at least one bug at the position."""
        return bool(self._grid.get(position))

    def remove_top_bug(self, position: Position) -> Bug | None:
        """Removes and returns the top bug at a given position."""
        stack = self._grid.get(position)
        if stack:
            return stack.pop()
        return None

    def can_place_bug(self, player: Player, position: Position) -> bool:
        """
        Checks whether a bug can be placed at the given position.

        Conditions:
        - The tile is empty
        - Bug must touch at least one of their own bugs
        - Bug may not touch any of the opponent's bugs
        - Exception: The first bug placed will not touch anything
        - Exception: The second bug placed will touch the first bug (of the opponent)
        - Exception: When beetle on top of stack, it takes on the colour of the Beetle
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

    def is_one_hive_after_removal(self, position: Position) -> bool:
        """Checks if hive remains connected after removing the top bug at given position."""
        # If nothing to remove, hive is unchanged
        if not self.is_occupied(position):
            return True

        # If position has more than 1 bug, the hive remains connected
        if len(self.get_stack(position)) > 1:
            return True

        # Temporarily remove top bug
        removed_bug = self.remove_top_bug(position)

        # Get all remaining occupied positions
        remaining = set(self.occupied_positions())
        # If no bugs remain, the hive is trivially connected
        if not remaining:
            self._grid[position].append(removed_bug)
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
        self._grid[position].append(removed_bug)

        # Check if all remaining positions were visited
        return visited == remaining

    def can_move_bug(self, bug: Bug, to_pos: Position) -> bool:
        """
        Determines if the given bug can legally move to the specified position.

        Checks:
        - Destination is different from current position
        - Bug is on top of its stack
        - One Hive: Hive remains connected after move
        - Movement logic (from behavior strategy) allows it
        - Freedom of Movement: Bug physically able to move to destination (one space at a time)
            - Usually means a piece must "slide" to its destination
            - Some configuration might leave a gap that is too narrow to pass
            - Climbing bug can be subject to this, if two tall stacks leave narrow gap
        """
        from hive.behaviors import get_behavior_for  # Lazy import to avoid circular dependency

        if bug.position == to_pos:
            return False

        # Check bug is on top of its stack
        stack = self.get_stack(bug.position)
        if not stack or stack[-1] != bug:
            return False

        # Check one hive rule
        if not self.is_one_hive_after_removal(bug.position):
            return False

        # Check movement rules via behavior strategy
        behavior = get_behavior_for(bug.bug_type)
        if to_pos not in behavior.get_valid_moves(bug, self):
            return False

        return True

    def move_bug(self, bug: Bug, to_pos: Position) -> bool:
        """
        Moves a bug to a new position if legal. Updates position and stack height.

        Returns:
            bool: True if moved successfully, False otherwise.
        """
        if not self.can_move_bug(bug, to_pos):
            return False

        self.remove_top_bug(bug.position)
        self.place_bug(bug, to_pos)
        return True

    def get_bug_at(self, position: Position) -> Bug | None:
        """Alias for get_top_bug — returns the bug on top at a position."""
        return self.get_top_bug(position)

    def get_all_bugs(self) -> list[Bug]:
        """Returns a flat list of all bugs on the board."""
        return [bug for stack in self._grid.values() for bug in stack]
