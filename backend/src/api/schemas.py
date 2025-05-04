from pydantic import BaseModel  # type: ignore


class PositionSchema(BaseModel):
    """Schema for representing a position in a 2D grid."""

    q: int
    r: int
