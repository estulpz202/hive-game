from enum import Enum

from hive.board import Board
from hive.models.bug import Bug
from hive.models.bugtype import BugType
from hive.models.player import Player
from hive.models.position import Position


class Phase(Enum):
    """Represents the different phases in the Hive game."""

    # Start of the game: queen placement, players can place (or move if queen placed)
    START = "Start"
    # Rest of the game: queens placed, players can place or move (or pass if neither possible)
    PLACE_MOVE = "PlaceOrMove"
    # The game has ended: nothing can be done
    GAME_OVER = "GameOver"

# The maximum number of bugs a player can place without placing their queen
MAX_PLACES_WO_QUEEN = 3

class Game:
    """
    Represents the full Hive game state and logic.

    Manages player turns, enforces turn rules, bug placements, movement, pass rules,
    queen placement timing, and win condition detection.
    """

    def __init__(self):
        self.board = Board()
        self.player_white = Player("WHITE")
        self.player_black = Player("BLACK")
        self.cur_player = self.player_white
        self.phase = Phase.START
        self.winner: Player | None = None
        self.draw: bool = False
        self.valid_positions = self.board.get_all_valid_positions(self.cur_player)
        self.valid_moves = self.board.get_all_valid_moves(self.cur_player)
        self.cur_player_passed = False
        self.prev_player_passed = False

    @property
    def opponent_player(self) -> Player:
        """Returns the opponent of the current player."""
        return self.player_black if self.cur_player == self.player_white else self.player_white

    def _check_game_end(self) -> bool:
        """Checks if the game should end and sets winner/draw accordingly."""
        def is_surrounded(player: Player) -> bool:
            queen = player.queen_bug
            if queen and queen.position:
                return all(self.board.is_occupied(nbor) for nbor in queen.position.neighbors())
            return False

        white_surrounded = is_surrounded(self.player_white)
        black_surrounded = is_surrounded(self.player_black)

        if ((white_surrounded and black_surrounded) or
            (self.prev_player_passed and self.cur_player_passed)):
            self.draw = True
            return True
        elif white_surrounded:
            self.winner = self.player_black
            return True
        elif black_surrounded:
            self.winner = self.player_white
            return True

        return False

    def switch_turn(self) -> None:
        """Switches to the next player's turn and checks for game end conditions."""
        if self.phase == Phase.GAME_OVER:
            return

        # Update the game state
        self.cur_player = self.opponent_player
        self.valid_positions = self.board.get_all_valid_positions(self.cur_player)
        self.valid_moves = self.board.get_all_valid_moves(self.cur_player)
        self.prev_player_passed = self.cur_player_passed
        self.cur_player_passed = self._can_player_pass()

        # Check if the game has ended
        if self._check_game_end():
            self.phase = Phase.GAME_OVER
            return

    def place_bug(self, bug_type: BugType, pos: Position) -> bool:
        """
        Attempts to place a bug from the current player's reserve.

        Enforces queen placement timing rule: queen must be placed by the 4th turn.

        Returns:
            bool: True on success, False on invalid move.
        """
        if self.phase == Phase.GAME_OVER or not self.valid_positions:
            print("Game is over or no valid positions available.")
            return False

        # Check if player has the bug in reserve
        player = self.cur_player
        if bug_type not in player.reserve:
            print(f"Bug type {bug_type} not in reserve.")
            return False

        # Enforce mandatory queen placement by player's 4th turn
        if not player.has_placed_queen:
            if len(player.placed) == MAX_PLACES_WO_QUEEN and bug_type != BugType.QUEEN_BEE:
                print("Queen must be placed by the 4th turn.")
                return False

        # Try to place the bug on the board
        bug = Bug(bug_type, player)
        print(f"Valid positions: {self.valid_positions}")
        if not self.board.place_bug(bug, pos, self.valid_positions):
            print(f"Invalid placement at {pos}.")
            return False

        # Update game phase if both queens placed
        if bug_type == BugType.QUEEN_BEE:
            if self.opponent_player.has_placed_queen:
                self.phase = Phase.PLACE_MOVE

        self.switch_turn()
        return True

    def move_bug(self, from_pos: Position, to_pos: Position) -> bool:
        """
        Attempts to move a bug owned by the current player.

        The player must have placed their queen before moving.

        Returns:
            bool: True on success, False otherwise.
        """
        player = self.cur_player
        if self.phase == Phase.GAME_OVER or not player.has_placed_queen or not self.valid_moves:
            return False

        # Check if the bug is owned by the current player
        bug = self.board.get_top_bug(from_pos)
        if not bug or bug.owner != player:
            return False

        # Try to move the bug
        if not self.board.move_bug(bug, to_pos, self.valid_moves):
            return False

        self.switch_turn()
        return True

    def _can_player_pass(self) -> bool:
        """Checks if the current player has no valid move or placement."""
        if self.phase == Phase.GAME_OVER:
            return False

        # Check if they can place any bug
        player = self.cur_player
        if player.reserve and self.valid_positions:
            return False

        # Check if they can move any placed bug
        if player.has_placed_queen and self.valid_moves:
            return False

        return True

    def force_pass(self) -> bool:
        """Forces a player to pass when no legal move is available."""
        if self.phase == Phase.GAME_OVER:
            return False

        if self.cur_player_passed:
            self.switch_turn()
            return True
        else:
            return False
