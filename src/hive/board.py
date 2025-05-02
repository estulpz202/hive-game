from collections import defaultdict
from collections.abc import Iterator

from hive.models.bug import Bug
from hive.models.position import Position


class Board:
    """
    Represents the Hive game board.

    Maintains bug positions, including stacked bugs (e.g., beetles),
    and provides utility methods for interacting with the board state.
    """

    def __init__(self):
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
