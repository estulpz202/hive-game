from hive.models.bug import Bug, BugType
from hive.models.player import Player
from hive.models.position import Position


def test_player_initialization():
    player = Player("white")
    assert player.color == "WHITE"
    assert len(player.reserve) == 11
    assert player.reserve.count(BugType.QUEEN_BEE) == 1
    assert player.reserve.count(BugType.ANT) == 3
    assert player.reserve.count(BugType.BEETLE) == 2
    assert player.reserve.count(BugType.SPIDER) == 2
    assert player.reserve.count(BugType.GRASSHOPPER) == 3
    assert player.placed == []


def test_remove_from_reserve_success():
    player = Player("black")
    assert BugType.ANT in player.reserve
    assert player.remove_from_reserve(BugType.ANT) is True
    assert player.reserve.count(BugType.ANT) == 2


def test_remove_from_reserve_failure():
    player = Player("black")
    for _ in range(3):
        player.remove_from_reserve(BugType.ANT)
    assert player.remove_from_reserve(BugType.ANT) is False


def test_add_to_placed():
    player = Player("white")
    bug = Bug(BugType.QUEEN_BEE, player, Position(0, 0))
    player.add_to_placed(bug)

    assert bug in player.placed


def test_has_not_placed_queen():
    player = Player("white")
    bug = Bug(BugType.SPIDER, player, Position(0, 0))
    player.add_to_placed(bug)

    assert player.has_placed_queen is False
