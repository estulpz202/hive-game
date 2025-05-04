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


def test_grassh_behavior_valid_moves(board, players):
    white, black = players
    center = Position(0, 0)
    west = Position(-1, 0)
    east = Position(1, 0)
    ee = Position(2, 0)

    eee = Position(3, 0)

    # grassh (w) - q1 (w) - q2 (b) - q3 (b)
    q1 = Bug(BugType.QUEEN_BEE, white)
    q2 = Bug(BugType.QUEEN_BEE, black)
    q3 = Bug(BugType.QUEEN_BEE, black)
    grassh = Bug(BugType.GRASSHOPPER, white)
    assert board.place_bug(q1, center)
    assert board.place_bug(q2, east)
    assert board.place_bug(q3, ee)
    assert board.place_bug(grassh, west)

    # Grassh should be able to jump over line of queens
    behavior = get_behavior_for(BugType.GRASSHOPPER)
    moves = behavior.get_valid_moves(grassh, board)
    expected_moves = {eee}

    assert len(moves) == len(expected_moves)
    assert set(moves) == expected_moves

    # Perform the move
    assert grassh.position == west
    assert board.move_bug(grassh, eee)
    assert grassh.position == eee
