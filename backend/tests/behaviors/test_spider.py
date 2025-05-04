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


def test_spider_behavior_valid_moves(board, players):
    white, black = players
    center = Position(0, 0)
    east = Position(1, 0)
    west = Position(-1, 0)

    right_se = Position(1, 1)
    right_ne = Position(2, -1)

    # spider (w) - q1 (w) - q2 (b)
    q1 = Bug(BugType.QUEEN_BEE, white)
    q2 = Bug(BugType.QUEEN_BEE, black)
    spider = Bug(BugType.SPIDER, white)
    assert board.place_bug(q1, center)
    assert board.place_bug(q2, east)
    assert board.place_bug(spider, west)

    behavior = get_behavior_for(BugType.SPIDER)
    moves = behavior.get_valid_moves(spider, board)

    # Spider should be able to move 3 spaces away following rules
    behavior = get_behavior_for(BugType.SPIDER)
    moves = behavior.get_valid_moves(spider, board)
    expected_moves = {right_se, right_ne}

    assert len(moves) == len(expected_moves)
    assert set(moves) == expected_moves

    # Perform the move
    assert spider.position == west
    assert board.move_bug(spider, right_ne)
    assert spider.position == right_ne
