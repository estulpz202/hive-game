"""Pydantic models for request/response payloads used in the Hive API."""

from collections import Counter

from pydantic import BaseModel  # type: ignore

from hive.game import Game, Phase
from hive.models.bug import Bug
from hive.models.player import Player

# JSON-serializable view model formats internal game state into structured JSON for the frontend,
# separating backend logic from presentation.

class BugView(BaseModel):
    """View model for a bug on the board."""

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

class RemainingBugsView(BaseModel):
    """View of how many of each bug type the player still has available."""

    bug_type: str
    count: int

class PlayerStateView(BaseModel):
    """View model of a player's state in the game."""

    color: str
    remaining_bugs: list[RemainingBugsView]
    queen_placed: bool

    @staticmethod
    def from_player(player: Player) -> "PlayerStateView":
        """Creates a PlayerStateView from a Player instance."""
        # Count bug types in the reserve
        bug_counts = Counter(player.reserve)

        remaining = [
            RemainingBugsView(bug_type=bug_type.value, count=count)
            for bug_type, count in bug_counts.items()
        ]
        return PlayerStateView(
            color=player.color,
            remaining_bugs=remaining,
            queen_placed=player.has_placed_queen
        )

class GameStateResponse(BaseModel):
    """View model for the current game state."""

    phase: str
    current_player: str
    bugs: list[BugView]
    players: list[PlayerStateView]
    can_pass: bool
    winner: str | None = None  # "White", "Black", or "Draw"

    @staticmethod
    def from_game(game: Game) -> "GameStateResponse":
        """Creates a GameStateResponse from a Game instance."""
        bugs = [BugView.from_bug(b) for b in game.board.get_all_bugs()]
        players = [PlayerStateView.from_player(game.player_white),
                   PlayerStateView.from_player(game.player_black)]
        winner = game.get_winner() if game.phase == Phase.GAME_OVER else None

        return GameStateResponse(
            phase=game.phase.value,
            current_player=game.cur_player.color,
            bugs=bugs,
            players=players,
            can_pass=game.cur_player_passed,
            winner=winner
        )

class PositionView(BaseModel):
    """View model for q/r coordinate for valid placements or movements."""

    q: int
    r: int

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
