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


def test_beetle_can_climb_on_adjacent_bug(board, players):
    white, black = players
    west = Position(-1, 0)
    center = Position(0, 0)
    east = Position(1, 0)

    nw = Position(0, -1)
    sw = Position(-1, 1)

    # beetle (w) - q1 (w) - q2 (b)
    q1 = Bug(BugType.QUEEN_BEE, white)
    q2 = Bug(BugType.QUEEN_BEE, black)
    beetle = Bug(BugType.BEETLE, white)
    assert board.place_bug(q1, center)
    assert board.place_bug(q2, east)
    assert board.place_bug(beetle, west)

    # Beetle should be able to climb and move like bee
    behavior = get_behavior_for(BugType.BEETLE)
    moves = behavior.get_valid_moves(beetle, board)
    expected_moves = {center, nw, sw}

    assert len(moves) == len(expected_moves)
    assert set(moves) == expected_moves

    # Perform the move
    assert beetle.position == west
    assert board.move_bug(beetle, center)
    assert beetle.position == center


def test_beetle_FOM(board, players):
    white, black = players
    center = Position(0, 0)
    west =  Position(-1, 0)
    ne = Position(1, -1)
    se = Position(0, 1)
    nw = Position(0, -1)
    sw = Position(-1, 1)

    east = Position(1, 0)
    behavior = get_behavior_for(BugType.BEETLE)

    # space - q1 (b)
    # beetle (w) - space
    beetle = Bug(BugType.BEETLE, white)
    q1 = Bug(BugType.QUEEN_BEE, black)
    assert board.place_bug(beetle, center)
    assert board.place_bug(q1, ne)

    expected_moves = {nw, ne, east} # Sliding: Only one blocker (east included)
    assert set(behavior.get_valid_moves(beetle, board)) == expected_moves

    # q_nw (w) - q1 (b)
    # sp - beetle (w) - sp
    q_nw = Bug(BugType.QUEEN_BEE, white)
    assert board.place_bug(q_nw, west)
    assert board.move_bug(q_nw, nw)
    # q_nw (w) - q1 (b)
    # q_w (w) - beetle (w) - sp
    # q_sw (w) - q2 (w)
    q_w = Bug(BugType.QUEEN_BEE, white)
    q_sw = Bug(BugType.QUEEN_BEE, white)
    q2 = Bug(BugType.QUEEN_BEE, white)
    assert board.place_bug(q_w, west)
    assert board.place_bug(q_sw, sw)
    assert board.place_bug(q2, se)

    expected_moves = {ne, nw, west, sw, se} # Sliding: Two blockers (east excluded)
    assert set(behavior.get_valid_moves(beetle, board)) == expected_moves

    # q_nw (w) - q1 (b)
    # q_w (w) - beetle (w) - beetle2 (w)
    # q_sw (w) - q2 (w)
    beetle2 = Bug(BugType.BEETLE, white)
    assert board.place_bug(beetle2, Position(1,1))
    assert board.move_bug(beetle2, east)

    assert east in behavior.get_valid_moves(beetle, board) # Climbing: No taller blockers

    # q_nw (w) - q1, b1 (b)
    # q_w (w) - beetle (w) - beetle2 (w)
    # q_sw (w) - q2 (w)
    b1 = Bug(BugType.BEETLE, black)
    assert board.place_bug(b1, Position(2,-2))
    assert board.move_bug(b1, ne)

    assert east in behavior.get_valid_moves(beetle, board) # Climbing: Only 1 taller blockers

    # q_nw (w) - q1, b1 (b)
    # q_w (w) - beetle (w) - beetle2 (w)
    # q_sw (w) - q2, b2 (w)
    b2 = Bug(BugType.BEETLE, white)
    assert board.place_bug(b2, Position(0,2))
    assert board.move_bug(b2, se)

    assert east not in behavior.get_valid_moves(beetle, board) # Climbing: 2 taller blockers