from hive.models.bug import Bug, BugType
from hive.models.player import Player
from hive.models.position import Position


def test_bug_initialization():
    player = Player("WHITE")
    bug = Bug(BugType.QUEEN_BEE, player)

    assert bug.bug_type == BugType.QUEEN_BEE
    assert bug.owner == player
    assert bug.position == None
    assert bug.height == -1


def test_bug_position_and_height_mutability():
    player = Player("BLACK")
    bug = Bug(BugType.ANT, player, Position(1, 1), height=-1)

    # Mutate position
    new_pos = Position(2, 2)
    bug.position = new_pos
    assert bug.position == new_pos

    # Mutate height
    bug.height = 1
    assert bug.height == 1


def test_bug_identity_not_field_equality():
    player = Player("WHITE")
    pos = Position(1, -1)

    bug1 = Bug(BugType.SPIDER, player, pos, height=0)
    bug2 = Bug(BugType.SPIDER, player, Position(1, -1), height=0)

    assert bug1 is not bug2  # identity check
    assert bug1 != bug2      # not equal
    assert bug1 is bug1      # identity check
    assert bug1 == bug1      # equal to itself


def test_bug_position_can_be_set_later():
    player = Player("WHITE")
    bug = Bug(BugType.GRASSHOPPER, player)

    assert bug.position is None
    bug.position = Position(0, 0)
    assert bug.position == Position(0, 0)
