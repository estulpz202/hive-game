import pytest  # type: ignore

from hive.behaviors import get_behavior_for
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

    # Perform the move
    assert queen.position == p1
    assert board.move_bug(queen, p3)
    assert queen.position == p3


def test_queen_FOM(board, players):
    """Queen should not be able to slide into a position if tightly blocked (FOM)."""
    white, black = players
    center = Position(0, 0)
    west = Position(-1, 0)
    northeast = Position(1, -1)
    southeast = Position(0, 1)
    northwest = Position(0, -1)
    southwest = Position(-1, 1)

    east = Position(1, 0)
    behavior = get_behavior_for(BugType.QUEEN_BEE)

    # space - blocker1 (b)
    # queen (w) - space
    queen = Bug(BugType.QUEEN_BEE, white)
    blocker1 = Bug(BugType.QUEEN_BEE, black)
    assert board.place_bug(queen, center)
    assert board.place_bug(blocker1, northeast)
    
    assert east in behavior.get_valid_moves(queen, board) # Only one blocker

    # queen_nw (w) - blocker1 (b)
    # space - queen (w) - space
    queen_nw = Bug(BugType.QUEEN_BEE, white)
    assert board.place_bug(queen_nw, west)
    assert board.move_bug(queen_nw, northwest)
    # queen_nw (w) - blocker1 (b)
    # q_w (w) - queen (w) - space
    # queen_sw (w) - blocker2 (w)
    q_w = Bug(BugType.QUEEN_BEE, white)
    queen_sw = Bug(BugType.QUEEN_BEE, white)
    blocker2 = Bug(BugType.QUEEN_BEE, white)
    assert board.place_bug(q_w, west)
    assert board.place_bug(queen_sw, southwest)
    assert board.place_bug(blocker2, southeast)

    assert east not in behavior.get_valid_moves(queen, board) # Two blockers
