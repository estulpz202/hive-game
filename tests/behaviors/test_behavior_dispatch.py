from hive.behaviors import get_behavior_for
from hive.behaviors.queen import QueenBehavior
from hive.models.bugtype import BugType


def test_get_behavior_for_returns_expected_types():
    assert isinstance(get_behavior_for(BugType.QUEEN_BEE), QueenBehavior)
