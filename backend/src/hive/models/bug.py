from dataclasses import dataclass
from typing import TYPE_CHECKING

from hive.models.bugtype import BugType
from hive.models.player import Player
from hive.models.position import Position

if TYPE_CHECKING:
    from hive.board import Board

# @dataclass is used to automatically generate special methods.
# Like __init__, __repr__, and __eq__ for the Bug class.
@dataclass(eq=False, unsafe_hash=True)
class Bug:
    """
    Represents a single bug token on the board.

    Each bug knows its type, owner, position, and stack height.
    """

    bug_type: BugType
    owner: Player
    position: Position | None = None  # Position is none before its placed
    height: int = -1  # -1 before its placed, 0 when on ground, >0 when stacked
    behavior = None  # Late-initialized BugBehavior instance for movement logic

    def get_valid_moves(self, board: "Board") -> list[Position]:
        """Delegate move logic to bug-specific behavior via strategy pattern."""
        if self.behavior is None:
            # Lazy import to break circular dependency
            from hive.behaviors import get_behavior_for
            self.behavior = get_behavior_for(self.bug_type)

        return self.behavior.get_valid_moves(self, board)

    def on_place(self) -> None:
        """Updates the owning player when this bug is placed on the board."""
        self.owner.remove_from_reserve(self.bug_type)
        self.owner.add_to_placed(self)
