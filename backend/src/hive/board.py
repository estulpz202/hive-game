from collections import defaultdict
from collections.abc import Iterator

from hive.models.bug import Bug
from hive.models.position import Position
from hive.rules import RuleEngine


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

    def get_stack(self, position: Position) -> list[Bug]:
        """Returns the bug stack at a given position."""
        return self._grid.get(position, [])

    def get_top_bug(self, position: Position) -> Bug | None:
        """Returns the top bug at a position, or None if empty."""
        stack = self._grid.get(position, [])
        return stack[-1] if stack else None

    def is_occupied(self, position: Position) -> bool:
        """Returns True if there is at least one bug at the position."""
        return bool(self._grid.get(position))

    def occupied_positions(self) -> Iterator[Position]:
        """Returns all positions that have at least one bug."""
        return (pos for pos, stack in self._grid.items() if stack)

    def place_bug(self, bug: Bug, pos: Position,
                  valid_places: set[Position] | None = None) -> bool:
        """
        Attempts to place a bug at a given position on the board.

        Args:
            bug (Bug): The bug to place.
            pos (Position): The target position to place the bug.
            valid_places (set[Position] | None): Optional precomputed legal positions.

        Returns:
            bool: True if the bug was successfully placed, False otherwise.
        """
        if not RuleEngine.can_place_bug(self, bug.owner, pos, valid_places):
            return False

        # Let the bug update its owner (remove from reserve, add to placed)
        bug.on_place()

        self._drop_bug(bug, pos)
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
        if not RuleEngine.can_move_bug(self, bug, to_pos, valid_moves):
            return False

        self.remove_top_bug(bug.position)
        self._drop_bug(bug, to_pos)
        return True
