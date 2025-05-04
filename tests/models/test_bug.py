from hive.models.bug import Bug, BugType
from hive.models.player import Player
from hive.models.position import Position


def test_bug_initialization():
    player = Player("WHITE")
    bug = Bug(BugType.QUEEN_BEE, player)

    assert bug.bug_type == BugType.QUEEN_BEE
    assert bug.owner == player
    assert bug.position == None


def test_bug_equality():
    player = Player("WHITE")
    pos = Position(1, -1)

    bug1 = Bug(BugType.ANT, player, pos)
    bug2 = Bug(BugType.ANT, player, Position(1, -1))

    assert bug1 == bug2


def test_bug_pos_changeable():
    player = Player("BLACK")
    pos1 = Position(2, 2)
    pos2 = Position(3, 3)

    bug = Bug(BugType.SPIDER, player, pos1)

    assert bug.position == pos1
    bug.position = pos2
    assert bug.position == pos2


def test_bug_position_is_mutable():
    player = Player("BLACK")
    bug = Bug(BugType.GRASSHOPPER, player, Position(0, 0))

    bug.position = Position(1, 0)
    assert bug.position == Position(1, 0)
