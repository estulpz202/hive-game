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


def test_ant_behavior_can_move_around_hive(board, players):
    white, black = players
    center = Position(0, 0)
    east = Position(1, 0)
    west = Position(-1, 0)
    
    sw = Position(-1, 1)
    nw = Position(0, -1)
    se = Position(0, 1)
    ne = Position(1, -1)

    right_e = Position(2, 0)
    right_se = Position(1, 1)
    right_ne = Position(2, -1)
    
    # Not included, disconnects destination
    # left_w = (-2, 0), left_sw = (-2, 1), left_nw = (-1, -1)

    # ant (w) - queen1 (w) - quee2 (b)
    queen1 = Bug(BugType.QUEEN_BEE, white)
    queen2 = Bug(BugType.QUEEN_BEE, black)
    ant = Bug(BugType.ANT, white)
    assert board.place_bug(queen1, center)
    assert board.place_bug(queen2, east)
    assert board.place_bug(ant, west)

    # Ant should be able to move around connected sides of hive
    behavior = get_behavior_for(BugType.ANT)
    moves = behavior.get_valid_moves(ant, board)
    expected_moves = {sw, nw, se, ne, right_e, right_se, right_ne}

    assert len(moves) == len(expected_moves)
    assert set(moves) == expected_moves

    # Perform the move
    assert ant.position == west
    assert board.move_bug(ant, right_ne)
    assert ant.position == right_ne


def test_ant_behavior_respects_FOM(board, players):
    """Queen should not be able to slide into a position if tightly blocked (FOM)."""
    white, black = players
    center = Position(0, 0)
    east = Position(1, 0)
    northeast = Position(1, -1)
    southeast = Position(0, 1)

    # space - queen (b)
    # ant (w)
    # space - queen (w)
    ant = Bug(BugType.ANT, white, center)
    blocker1 = Bug(BugType.QUEEN_BEE, black, northeast)
    blocker2 = Bug(BugType.QUEEN_BEE, white, southeast)

    assert board.place_bug(ant, center)
    assert board.place_bug(blocker1, northeast)
    assert board.place_bug(blocker2, southeast)

    behavior = get_behavior_for(BugType.ANT)
    moves = behavior.get_valid_moves(ant, board)

    # Tile east of ant is blocked by tight gap
    assert east not in moves


def test_ant_behavior_no_moves_if_breaks_hive(board, players):
    white, black = players
    center = Position(0, 0)
    east = Position(1, 0)
    west = Position(-1, 0)

    # queen1 (b) - ant (w) - quee2 (w)
    ant = Bug(BugType.ANT, white)
    queen1 = Bug(BugType.QUEEN_BEE, black)
    queen2 = Bug(BugType.QUEEN_BEE, white)
    assert board.place_bug(ant, center)
    assert board.place_bug(queen1, west)
    assert board.place_bug(queen2, east)

    behavior = get_behavior_for(BugType.ANT)
    assert behavior.get_valid_moves(ant, board) == []
