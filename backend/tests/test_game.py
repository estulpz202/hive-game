from hive.game import Game, Phase
from hive.models.bugtype import BugType
from hive.models.position import Position


def test_game_initialization():
    game = Game()
    assert game.phase == Phase.START
    assert game.cur_player.color == "WHITE"
    assert game.opponent_player.color == "BLACK"
    assert game.winner is None
    assert game.draw is False
    assert isinstance(game.valid_positions, set)
    assert isinstance(game.valid_moves, dict)


def test_place_bug_success_and_turn_switch():
    game = Game()
    pos = Position(0, 0)

    assert game.place_bug(BugType.QUEEN_BEE, pos)
    assert game.cur_player.color == "BLACK"  # Turn switched


def test_place_bug_illegal_without_queen_by_turn_4():
    game = Game()

    # white center, black left of center, white right of center
    white_positions = [Position(q, 0) for q in range(3)]
    black_positions = [Position(-q, 0) for q in range(1, 4)]
    for w_pos, b_pos in zip(white_positions, black_positions):
        assert game.place_bug(BugType.ANT, w_pos)
        assert game.place_bug(BugType.ANT, b_pos)

    # Fourth placement must be queen, else illegal
    assert not game.place_bug(BugType.SPIDER, Position(3, 0))
    assert game.place_bug(BugType.QUEEN_BEE, Position(3, 0))

    assert not game.place_bug(BugType.SPIDER, Position(-4, 0))
    assert game.place_bug(BugType.QUEEN_BEE, Position(-4, 0))


def test_game_phase_switches_after_both_queens():
    game = Game()

    assert game.phase == Phase.START
    assert game.place_bug(BugType.QUEEN_BEE, Position(0, 0))  # White
    assert game.phase == Phase.START
    assert game.place_bug(BugType.QUEEN_BEE, Position(1, 0))  # Black
    assert game.phase == Phase.PLACE_MOVE


def test_move_bug_fail_before_placing_queen():
    game = Game()
    wpos = Position(0, 0)
    bpos = Position(1, 0)

    # Place ants without placing queen first
    assert game.place_bug(BugType.ANT, wpos)
    assert game.place_bug(BugType.ANT, bpos)

    # Now try to move it (should fail)
    from_pos = wpos
    to_pos = Position(0, 1)
    assert not game.move_bug(from_pos, to_pos)


def test_move_bug_success_after_queen():
    game = Game()

    # White places queen
    assert game.place_bug(BugType.QUEEN_BEE, Position(0, 0))
    # Black places queen
    assert game.place_bug(BugType.QUEEN_BEE, Position(1, 0))

    # White places ANT
    assert game.place_bug(BugType.ANT, Position(-1, 0))
    # Black places ANT
    assert game.place_bug(BugType.ANT, Position(2, 0))

    # White moves ANT
    from_pos = Position(-1, 0)
    to_pos = Position(-1, 1)
    assert game.move_bug(from_pos, to_pos)


def test_force_pass_when_no_move_or_place():
    game = Game()
    game.phase = Phase.PLACE_MOVE

    # Place queens
    assert game.place_bug(BugType.QUEEN_BEE, Position(0, 0))
    assert game.cur_player.color == "BLACK"
    assert game.place_bug(BugType.QUEEN_BEE, Position(1, 0))
    assert game.cur_player.color == "WHITE"

    # Simulate empty reserve and no moves
    game.valid_positions = set()
    game.valid_moves = {}
    game.cur_player_passed = game._can_player_pass()

    assert game.cur_player_passed is True
    assert game.force_pass()
    assert game.cur_player.color == "BLACK" # Turn switches to other player


def test_game_draw(monkeypatch):
    game = Game()

    # Patch is_surrounded to return True for both players
    monkeypatch.setattr(game.board, "is_occupied", lambda pos: True)
    monkeypatch.setattr(game, "_check_game_end", lambda: True)
    game.draw = True
    game.phase = Phase.PLACE_MOVE

    game.switch_turn()
    assert game.phase == Phase.GAME_OVER
    assert game.draw is True
    assert game.winner is None


def test_game_win(monkeypatch):
    game = Game()

    game.phase = Phase.PLACE_MOVE
    game.cur_player = game.player_white
    game.prev_player_passed = False
    game.cur_player_passed = False

    monkeypatch.setattr(game, "_check_game_end", lambda: True)
    game.winner = game.player_white
    game.switch_turn()

    assert game.phase == Phase.GAME_OVER
    assert game.winner.color == "WHITE"
