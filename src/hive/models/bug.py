from dataclasses import dataclass
from enum import Enum

from hive.models.player import Player
from hive.models.position import Position


class BugType(Enum):
    """BugType enumeration."""

    QUEEN_BEE = "QueenBee"
    ANT = "Ant"
    BEETLE = "Beetle"
    SPIDER = "Spider"
    GRASSHOPPER = "Grasshopper"

@dataclass
class Bug:
    """Represents a bug on the board."""

    bug_type: BugType
    owner: Player  # "WHITE" or "BLACK"
    position: Position
    on_top: int = 0  # 0 = ground level, 1+ = stack height
