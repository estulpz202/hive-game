from hive.behaviors import get_behavior_for
from hive.behaviors.ant import AntBehavior
from hive.behaviors.beetle import BeetleBehavior
from hive.behaviors.grasshopper import GrasshopperBehavior
from hive.behaviors.queen import QueenBehavior
from hive.behaviors.spider import SpiderBehavior
from hive.models.bugtype import BugType


def test_get_behavior_for_returns_expected_types():
    assert isinstance(get_behavior_for(BugType.QUEEN_BEE), QueenBehavior)
    assert isinstance(get_behavior_for(BugType.ANT), AntBehavior)
    assert isinstance(get_behavior_for(BugType.SPIDER), SpiderBehavior)
    assert isinstance(get_behavior_for(BugType.BEETLE), BeetleBehavior)
    assert isinstance(get_behavior_for(BugType.GRASSHOPPER), GrasshopperBehavior)
