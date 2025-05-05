"""Defines and registers all API routes for the Hive backend."""

from fastapi import APIRouter, Query  # type: ignore

from api.models import GameStateResponse, MoveBugRequest, PlaceBugRequest, PositionView
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

@api_router.get("/valid-placements", response_model=list[PositionView])
def get_valid_placements(bug_type: str = Query(...)):
    """Returns valid placement positions considering queen placement rules."""
    bt = BugType(bug_type)
    valid_pos = game.valid_positions(bt)
    return [PositionView(q=p.q, r=p.r) for p in valid_pos]

@api_router.get("/valid-moves", response_model=list[PositionView])
def get_valid_moves(q: int = Query(...), r: int = Query(...)):
    """Returns valid destination positions for a selected bug."""
    from_pos = Position(q, r)
    bug = game.board.get_top_bug(from_pos)

    valid_moves = game.valid_moves.get(bug, [])
    return [PositionView(q=pos.q, r=pos.r) for pos in valid_moves]

# POST endpoint sends data to the server to create or change state.

@api_router.post("/newgame")
def new_game():
    """Resets the game to initial state."""
    global game # allow modifying the shared game across endpoints
    game = Game()
    return GameStateResponse.from_game(game)

@api_router.post("/place")
def place_bug(request: PlaceBugRequest):
    """Places a bug on the board."""
    bug_type = BugType(request.bug_type)
    pos = Position(request.q, request.r)
    game.place_bug(bug_type, pos)
    return GameStateResponse.from_game(game)

@api_router.post("/move")
def move_bug(request: MoveBugRequest):
    """Moves a bug from one position to another."""
    from_pos = Position(request.from_q, request.from_r)
    to_pos = Position(request.to_q, request.to_r)
    game.move_bug(from_pos, to_pos)
    return GameStateResponse.from_game(game)

@api_router.post("/pass")
def pass_turn():
    """Forces the current player to pass if no valid move/place."""
    game.force_pass()
    return GameStateResponse.from_game(game)
