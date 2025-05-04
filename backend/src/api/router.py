"""Defines and registers all API routes for the Hive backend."""

from fastapi import APIRouter, HTTPException  # type: ignore

from api.models import GameStateResponse, MoveBugRequest, PlaceBugRequest
from hive.game import Game
from hive.models.bugtype import BugType
from hive.models.position import Position

# Create a router instance
api_router = APIRouter()
# Initialize the game instance
game = Game()

# GET endpoint retrieves data without modifying the server.

@api_router.get("/state", response_model=GameStateResponse)
def get_state():
    """Returns the current game state."""
    return GameStateResponse.from_game(game)

# POST endpoint sends data to the server to create or change state.

@api_router.post("/place")
def place_bug(request: PlaceBugRequest):
    """Places a bug on the board."""
    bug_type = BugType(request.bug_type)
    pos = Position(request.q, request.r)
    if not game.place_bug(bug_type, pos):
        raise HTTPException(status_code=400, detail="Invalid placement")
    return {"success": True}

@api_router.post("/move")
def move_bug(request: MoveBugRequest):
    """Moves a bug from one position to another."""
    from_pos = Position(request.from_q, request.from_r)
    to_pos = Position(request.to_q, request.to_r)
    if not game.move_bug(from_pos, to_pos):
        raise HTTPException(status_code=400, detail="Invalid move")
    return {"success": True}
