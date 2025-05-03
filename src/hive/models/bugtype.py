from enum import Enum


# Enum is a class that allows the creation of enumerations.
# A set of symbolic names bound to unique, constant values.
class BugType(Enum):
    """Enumeration of all bug types in the Hive base game."""

    QUEEN_BEE = "QueenBee"
    ANT = "Ant"
    BEETLE = "Beetle"
    SPIDER = "Spider"
    GRASSHOPPER = "Grasshopper"
