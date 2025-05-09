import pytest  # type: ignore

from hive.board import Board
from hive.models.bug import Bug, BugType
from hive.models.player import Player
from hive.models.position import Position
from hive.rules import RuleEngine

@pytest.fixture
def board():
    return Board()

@pytest.fixture
def players():
    return Player("WHITE"), Player("BLACK")

def test_cannot_place_on_occupied(board, players):
    white, _ = players
    pos = Position(0, 0)
    bug1 = Bug(BugType.QUEEN_BEE, white, pos)
    bug2 = Bug(BugType.ANT, white, pos)

    assert board.place_bug(bug1, pos)
    assert not RuleEngine.can_place_bug(board, white, pos)
    assert not board.place_bug(bug2, pos)

def test_can_place_first_bug(board, players):
    white, _ = players
    pos = Position(0, 0)
    assert RuleEngine.can_place_bug(board, white, pos)

def test_can_place_second_bug_adjacent_to_opponent(board, players):
    white, black = players
    p1 = Position(0, 0)
    p2 = Position(1, 0)

    bug1 = Bug(BugType.QUEEN_BEE, black, p1)
    bug2 = Bug(BugType.QUEEN_BEE, white, p2)

    assert board.place_bug(bug1, p1)
    assert RuleEngine.can_place_bug(board, white, p2)
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
    assert not RuleEngine.can_place_bug(board, white, p3)
    assert not RuleEngine.can_place_bug(board, white, p4)

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
    assert RuleEngine.can_place_bug(board, white, p3)
    assert board.place_bug(bug3, p3)

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

    assert RuleEngine.can_slide_to(board, p2, p3)
    assert RuleEngine.can_slide_to(board, p1, p3)
    assert not RuleEngine.can_slide_to(board, p1, p4)
    assert not RuleEngine.can_slide_to(board, p1, p5)

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

    assert RuleEngine.is_one_hive_move(board, p1)
    assert RuleEngine.is_one_hive_move(board, p1, p4)
    assert not RuleEngine.dest_is_connected(board, p1, p5)
    assert not RuleEngine.is_one_hive_move(board, p1, p5)

def test_can_move_bug_and_move_bug(board, players):
    white, black = players
    p1 = Position(0, 0)
    p2 = Position(1, 0)
    p3 = Position(1, -1)
    p4 = Position(0, 1)

    white_bug = Bug(BugType.QUEEN_BEE, white, p2)
    black_bug = Bug(BugType.QUEEN_BEE, black, p1)

    assert board.place_bug(black_bug, p1)
    assert board.place_bug(white_bug, p2)

    assert RuleEngine.can_move_bug(board, white_bug, p4)
    assert RuleEngine.can_move_bug(board, white_bug, p3)
    assert board.move_bug(white_bug, p3)

    assert board.get_top_bug(p3) == white_bug
    assert not board.is_occupied(p2)

def test_get_all_valid_positions_initial(board, players):
    white, _ = players
    assert RuleEngine.get_all_valid_places(board, white) == {Position(0, 0)}

def test_get_all_valid_positions_second_bug(board, players):
    white, black = players
    pos = Position(0, 0)
    queen = Bug(BugType.QUEEN_BEE, black)
    assert board.place_bug(queen, pos)

    expected = set(pos.neighbors())
    result = RuleEngine.get_all_valid_places(board, white)
    assert result == expected

def test_get_all_valid_positions_own_neighbors_only(board, players):
    white, black = players
    center = Position(0, 0)
    east = Position(1, 0)
    west = Position(-1, 0)

    white_q = Bug(BugType.QUEEN_BEE, white)
    black_q = Bug(BugType.QUEEN_BEE, black)
    white_ant = Bug(BugType.ANT, white)

    assert board.place_bug(white_q, center)
    assert board.place_bug(black_q, east)
    assert board.place_bug(white_ant, west)

    legal = RuleEngine.get_all_valid_places(board, white)

    nw = Position(0, -1)
    sw = Position(-1, 1)
    left_w = Position(-2, 0)
    left_nw = Position(-1, -1)
    left_sw = Position(-2, 1)
    expected = {nw, left_nw, left_w, left_sw, sw}

    assert legal == expected

def test_get_all_valid_moves_requires_queen(board, players):
    white, _ = players
    bug = Bug(BugType.ANT, white)
    assert board.place_bug(bug, Position(0, 0))

    assert RuleEngine.get_valid_moves(board, white) == {}

def test_get_all_valid_moves_skips_bugs_not_on_top(board, players):
    white, _ = players
    queen = Bug(BugType.QUEEN_BEE, white)
    ant = Bug(BugType.ANT, white)
    assert board.place_bug(queen, Position(0, 0))
    board._drop_bug(ant, Position(0, 0))  # Now queen is covered
    white.remove_from_reserve(ant.bug_type)
    white.add_to_placed(ant)
    assert white.has_placed_queen
    assert white.queen_bug == queen

    moves = RuleEngine.get_valid_moves(board, white)
    assert queen not in moves
    assert ant in moves

def test_get_all_valid_moves_returns_correct_structure(board, players):
    white, black = players
    queen = Bug(BugType.QUEEN_BEE, white)
    enemy = Bug(BugType.QUEEN_BEE, black)

    pos1 = Position(0, 0)
    pos2 = Position(1, 0)

    assert board.place_bug(queen, pos1)
    board._drop_bug(enemy, pos2)

    assert white.queen_bug == queen
    assert white.has_placed_queen

    moves = RuleEngine.get_valid_moves(board, white)

    assert isinstance(moves, dict)
    assert queen in moves
    assert isinstance(moves[queen], list)
    assert all(isinstance(p, Position) for p in moves[queen])
    assert set([Position(1, -1), Position(0, 1)]) == set(moves[queen])
