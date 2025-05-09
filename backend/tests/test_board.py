import pytest  # type: ignore

from hive.board import Board
from hive.models.bug import Bug, BugType
from hive.models.player import Player
from hive.models.position import Position

@pytest.fixture
def board():
    return Board()

@pytest.fixture
def players():
    return Player("WHITE"), Player("BLACK")

def test_drop_bug_assigns_position_and_stack_height(board, players):
    white, _ = players
    pos = Position(2, -2)

    bug1 = Bug(BugType.ANT, white)
    bug2 = Bug(BugType.SPIDER, white)

    board._drop_bug(bug1, pos)
    board._drop_bug(bug2, pos)

    stack = board.get_stack(pos)

    assert bug1.position == pos
    assert bug2.position == pos
    assert stack == [bug1, bug2]

def test_place_and_get_top_bug(board, players):
    white, _ = players
    pos = Position(0, 0)
    bug = Bug(BugType.QUEEN_BEE, white, pos)

    assert board.place_bug(bug, pos)
    assert board.get_top_bug(pos) == bug

def test_get_stack(board, players):
    white, _ = players
    pos = Position(0, 0)
    bug = Bug(BugType.QUEEN_BEE, white, pos)

    assert board.place_bug(bug, pos)
    assert board.get_stack(pos) == [bug]

def test_remove_top_bug(board, players):
    white, _ = players
    pos = Position(0, 0)
    bug = Bug(BugType.ANT, white, pos)

    board.place_bug(bug, pos)
    removed = board._remove_top_bug(pos)
    assert removed == bug
    assert board.get_top_bug(pos) is None

def test_occupied_positions_and_is_occupied(board, players):
    white, _ = players
    pos = Position(0, 0)
    bug = Bug(BugType.SPIDER, white, pos)

    assert not board.is_occupied(pos)
    board.place_bug(bug, pos)
    assert board.is_occupied(pos)
    assert list(board.occupied_positions()) == [pos]

def test_move_bug_and_updates_position(board, players):
    white, black = players
    p1 = Position(0, 0)
    p2 = Position(1, 0)
    p3 = Position(1, -1)

    white_bug = Bug(BugType.QUEEN_BEE, white)
    black_bug = Bug(BugType.QUEEN_BEE, black)

    board.place_bug(black_bug, p1)
    board.place_bug(white_bug, p2)

    assert board.move_bug(white_bug, p3)
    assert board.get_top_bug(p3) == white_bug
    assert not board.is_occupied(p2)
