import pytest  # type: ignore

from hive.behaviors import get_behavior_for
from hive.behaviors.queen import QueenBehavior
from hive.board import Board
from hive.models.bug import Bug
from hive.models.bugtype import BugType
from hive.models.player import Player
from hive.models.position import Position


@pytest.fixture
def board():
    return Board()


@pytest.fixture
def players():
    return Player("WHITE"), Player("BLACK")


def test_get_behavior_for_returns_expected_types():
    assert isinstance(get_behavior_for(BugType.QUEEN_BEE), QueenBehavior)


def test_queen_behavior_valid_moves(board, players):
    white, black = players
    p1 = Position(0, 0)
    p2 = Position(1, 0)
    p3 = Position(0, 1)

    queen = Bug(BugType.QUEEN_BEE, white, p1)
    neighbor = Bug(BugType.QUEEN_BEE, black, p2)

    assert board.place_bug(queen, p1)
    assert board.place_bug(neighbor, p2)

    behavior = get_behavior_for(BugType.QUEEN_BEE)
    moves = behavior.get_valid_moves(queen, board)

    # Queen should be able to slide to p3 (unoccupied, adjacent, valid)
    assert p3 in moves
    # Queen should not be able to move to p2 (occupied)
    assert p2 not in moves


def test_queen_behavior_blocked_slide(board, players):
    """Queen should not be able to slide into a position if tightly blocked (FOM)."""
    white, black = players
    center = Position(0, 0)
    east = Position(1, 0)
    northeast = Position(1, -1)
    southeast = Position(0, 1)

    queen = Bug(BugType.QUEEN_BEE, white, center)
    blocker1 = Bug(BugType.QUEEN_BEE, black, northeast)
    blocker2 = Bug(BugType.QUEEN_BEE, white, southeast)

    assert board.place_bug(queen, center)
    assert board.place_bug(blocker1, northeast)
    assert board.place_bug(blocker2, southeast)

    behavior = get_behavior_for(BugType.QUEEN_BEE)
    moves = behavior.get_valid_moves(queen, board)

    # Queen cannot slide east because both shared neighbors are blocked
    assert east not in moves
