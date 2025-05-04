"""Pydantic models for request/response payloads used in the Hive API."""

from pydantic import BaseModel  # type: ignore

from hive.game import Game
from hive.models.bug import Bug

# JSON-serializable view model formats internal game state into structured JSON for the frontend,
# separating backend logic from presentation.

class BugView(BaseModel):
    """JSON view model for a bug on the board."""

    bug_type: str
    owner: str
    q: int
    r: int
    height: int

    @staticmethod
    def from_bug(bug: Bug) -> "BugView":
        """Creates a BugView from a Bug instance."""
        return BugView(
            bug_type=bug.bug_type.value,
            owner=bug.owner.color,
            q=bug.position.q,
            r=bug.position.r,
            height=bug.height,
        )

class GameStateResponse(BaseModel):
    """JSON view model for the current game state."""

    phase: str
    current_player: str
    bugs: list[BugView]

    @staticmethod
    def from_game(game: Game) -> "GameStateResponse":
        """Creates a GameStateResponse from a Game instance."""
        bugs = [BugView.from_bug(bug) for bug in game.board.get_all_bugs()]
        return GameStateResponse(
            phase=game.phase.value,
            current_player=game.cur_player.color,
            bugs=bugs,
        )

# Request DTO (Data Transfer Object) is a structured object that defines the data a client must
# send when calling endpoints. It separates incoming data from internal logic.

class PlaceBugRequest(BaseModel):
    """Request DTO for placing a bug on the board."""

    bug_type: str
    q: int
    r: int

class MoveBugRequest(BaseModel):
    """Request DTO for moving a bug from one position to another."""

    from_q: int
    from_r: int
    to_q: int
    to_r: int
