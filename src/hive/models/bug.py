from dataclasses import dataclass
from enum import Enum

from hive.models.player import Player
from hive.models.position import Position


# Enum is a class that allows the creation of enumerations.
# A set of symbolic names bound to unique, constant values.
class BugType(Enum):
    """Enumeration of all bug types in the Hive base game."""

    QUEEN_BEE = "QueenBee"
    ANT = "Ant"
    BEETLE = "Beetle"
    SPIDER = "Spider"
    GRASSHOPPER = "Grasshopper"


# @dataclass is used to automatically generate special methods.
# Like __init__, __repr__, and __eq__ for the Bug class.
@dataclass
class Bug:
    """
    Represents a single bug token on the board.

    Each bug knows its type, owner, position, and stack height.
    """

    bug_type: BugType
    owner: Player
    position: Position
    on_top: int = 0  # 0 = ground level, 1+ = height in stack
