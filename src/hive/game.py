class Game:
    """
    Coordinates the game.

    Manages turns, checks for win conditions, and orchestrates
    interactions between players and the board.
    """

    def __init__(self):
        self.board = None  # Will be Board instance
        self.players = []
        self.turn = 0
