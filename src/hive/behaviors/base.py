from abc import ABC, abstractmethod

from hive.board import Board
from hive.models.bug import Bug
from hive.models.position import Position


class BugBehavior(ABC):
    """Base class for bug movement behavior using the Strategy pattern."""

    @abstractmethod
    def get_valid_moves(self, bug: Bug, board: Board) -> list[Position]:
        """
        Returns a list of valid positions this bug can move to.

        Args:
            bug (Bug): The bug attempting to move.
            board (Board): The current game board.

        Returns:
            list[Position]: Valid destination positions.
        """
        pass
