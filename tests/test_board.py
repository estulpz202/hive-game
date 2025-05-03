import pytest # type: ignore

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


def test_place_and_get_top_bug(board, players):
    white, _ = players
    pos = Position(0, 0)
    bug = Bug(BugType.QUEEN_BEE, white, pos)

    assert board.place_bug(bug, pos)
    assert board.get_top_bug(pos) == bug


def test_get_stack_and_bug_at(board, players):
    white, _ = players
    pos = Position(0, 0)
    bug = Bug(BugType.QUEEN_BEE, white, pos)

    assert board.place_bug(bug, pos)

    assert board.get_stack(pos) == [bug]
    assert board.get_bug_at(pos) == bug


def test_remove_top_bug(board, players):
    white, _ = players
    pos = Position(0, 0)
    bug = Bug(BugType.ANT, white, pos)

    board.place_bug(bug, pos)
    removed = board.remove_top_bug(pos)
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


def test_cannot_place_on_occupied(board, players):
    white, _ = players
    pos = Position(0, 0)
    bug1 = Bug(BugType.QUEEN_BEE, white, pos)
    bug2 = Bug(BugType.ANT, white, pos)

    assert board.place_bug(bug1, pos)
    assert not board.can_place_bug(white, pos)
    assert not board.place_bug(bug2, pos)


def test_can_place_first_bug_anywhere(board, players):
    white, _ = players
    pos = Position(3, -3)
    assert board.can_place_bug(white, pos)


def test_can_place_second_bug_adjacent_to_opponent(board, players):
    white, black = players
    p1 = Position(0, 0)
    p2 = Position(1, 0)

    bug1 = Bug(BugType.QUEEN_BEE, black, p1)
    bug2 = Bug(BugType.QUEEN_BEE, white, p2)

    assert board.place_bug(bug1, p1)
    assert board.can_place_bug(white, p2)
    assert board.place_bug(bug2, p2)


def test_place_third_bug_incorrectly(board, players):
    white, black = players
    p1 = Position(0, 0)
    p2 = Position(1, 0)
    p3 = Position(1, -1)
    p4 = Position(-1, 0)

    bug1 = Bug(BugType.QUEEN_BEE, black, p1)
    bug2 = Bug(BugType.QUEEN_BEE, white, p2)

    assert board.place_bug(bug1, p1)
    assert board.place_bug(bug2, p2)
    assert not board.can_place_bug(white, p3)  # p3 is adjacent to both bugs
    assert not board.can_place_bug(white, p4)  # p4 is not adjacent to white bug


def test_place_third_bug_correctly(board, players):
    white, black = players
    p1 = Position(0, 0)
    p2 = Position(1, 0)
    p3 = Position(2, 0)

    bug1 = Bug(BugType.QUEEN_BEE, black, p1)
    bug2 = Bug(BugType.QUEEN_BEE, white, p2)
    bug3 = Bug(BugType.ANT, white, p3)

    assert board.place_bug(bug1, p1)
    assert board.place_bug(bug2, p2)
    assert board.can_place_bug(white, p3)  # p3 is adjacent to white's bug
    assert board.place_bug(bug3, p3)


def test_get_all_bugs(board, players):
    white, black = players
    p1 = Position(0, 0)
    p2 = Position(1, 0)

    bug1 = Bug(BugType.QUEEN_BEE, black, p1)
    bug2 = Bug(BugType.ANT, white, p2)

    assert board.place_bug(bug1, p1)
    assert board.place_bug(bug2, p2)

    all_bugs = board.get_all_bugs()
    assert len(all_bugs) == 2
    assert bug1 in all_bugs
    assert bug2 in all_bugs


def test_can_slide_to(board, players):
    white, black = players
    p1 = Position(0, 0)
    p2 = Position(1, 0)
    p3 = Position(1, -1)
    p4 = Position(2, 0)
    p5 = Position(0, 2)

    bug1 = Bug(BugType.QUEEN_BEE, black, p1)
    bug2 = Bug(BugType.ANT, white, p2)

    assert board.place_bug(bug1, p1)
    assert board.place_bug(bug2, p2)

    assert board.can_slide_to(p2, p3)  # p3 is adjacent, unoccupied, keeps OHR
    assert board.can_slide_to(p1, p3)

    assert not board.can_slide_to(p1, p4)  # p4 is not adjacent to p1
    assert not board.can_slide_to(p1, p5)  # p5 not adjacent to p1 and not OHR
    assert not board.can_slide_to(p1, p2)  # p2 occupied


def test_is_one_hive_move_and_dest_is_connected(board, players):
    white, black = players
    p1 = Position(0, 0)
    p2 = Position(1, 0)
    p3 = Position(2, 0)
    p4 = Position(1, -1)
    p5 = Position(-1, 1)

    bug1 = Bug(BugType.QUEEN_BEE, black, p1)
    bug2 = Bug(BugType.QUEEN_BEE, white, p2)
    bug3 = Bug(BugType.ANT, white, p3)

    assert board.place_bug(bug1, p1)
    assert board.place_bug(bug2, p2)
    assert board.place_bug(bug3, p3)

    assert board.is_one_hive_move(p1)  # Removing bug1 keeps the hive connected
    assert board.is_one_hive_move(p1, p4)  # Moving bug1 to p4 keeps the hive connected

    assert not board.dest_is_connected(p1, p5) # Moving bug1 to p5 disconnected bug1
    assert not board.is_one_hive_move(p1, p5)  # Moving bug1 to p5 disconnects the hive

def test_can_move_bug_and_move_bug(board, players):
    white, black = players
    p1 = Position(0, 0)
    p2 = Position(1, 0)
    p3 = Position(1, -1)
    p4 = Position(0, 1)

    # Each player places a Queen Bee
    white_bug = Bug(BugType.QUEEN_BEE, white, p2)
    black_bug = Bug(BugType.QUEEN_BEE, black, p1)

    assert board.place_bug(black_bug, p1)
    assert board.place_bug(white_bug, p2)

    # Now try to move white's bug to p3
    assert board.can_move_bug(white_bug, p4)
    assert board.can_move_bug(white_bug, p3)
    assert board.move_bug(white_bug, p3)

    assert board.get_top_bug(p3) == white_bug
    assert not board.is_occupied(p2)

