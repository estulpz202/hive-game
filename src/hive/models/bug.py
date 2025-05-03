from dataclasses import dataclass

from hive.models.bugtype import BugType
from hive.models.player import Player
from hive.models.position import Position


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
    position: Position | None = None # Position is none before its placed
    on_top: int = 0  # 0 = ground level, >0 = height in stack
