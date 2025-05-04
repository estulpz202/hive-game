"""Behavior dispatch for bug movement logic."""

from hive.behaviors.ant import AntBehavior
from hive.behaviors.base import BugBehavior
from hive.behaviors.beetle import BeetleBehavior
from hive.behaviors.grasshopper import GrasshopperBehavior
from hive.behaviors.queen import QueenBehavior
from hive.behaviors.spider import SpiderBehavior
from hive.models.bugtype import BugType

_behavior_map: dict[BugType, BugBehavior] = {
    BugType.QUEEN_BEE: QueenBehavior(),
    BugType.ANT: AntBehavior(),
    BugType.BEETLE: BeetleBehavior(),
    BugType.GRASSHOPPER: GrasshopperBehavior(),
    BugType.SPIDER: SpiderBehavior(),
}


def get_behavior_for(bug_type: BugType) -> BugBehavior:
    """Returns the behavior strategy associated with a bug type."""
    return _behavior_map[bug_type]
