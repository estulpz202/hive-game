from hive.behaviors.base import BugBehavior
from hive.board import Board
from hive.models.bug import Bug
from hive.models.position import Position


class GrasshopperBehavior(BugBehavior):
    """Movement rules for the Grasshopper: jump over a line and land on the first empty space."""

    def get_valid_moves(self, bug: Bug, board: Board) -> list[Position]:
        """
        Returns valid jump destinations for the grasshopper.

        Conditions: Removing grasshopper obeys OHR (dest trivially always obeys OHR),
        jumps in a straight line over at least one occupied space, land on first unoccupied tile,
        and can jump over stacks and ignore gates.

        Args:
            bug (Bug): The grasshopper bug.
            board (Board): The game board.

        Returns:
            list[Position]: Valid destinations for the grasshopper.
        """
        # Check one hive rule for removing bug
        if not board.is_one_hive_move(bug.position):
            return []

        valid = []

        # Loop over the 6 possible hex directions by checking each neighbor
        for direction in bug.position.neighbors():
            # Compute direction vector
            dq = direction.q - bug.position.q
            dr = direction.r - bug.position.r

            cur = bug.position
            have_jumped = False

            # Step forward repeatedly in the same direction
            while True:
                cur = Position(cur.q + dq, cur.r + dr)

                # If we reach an empty tile
                if not board.is_occupied(cur):
                    # Check if we've jumped over at least one tile
                    if have_jumped:
                        valid.append(cur)
                    break  # Stop exploring this direction
                else:
                    # Keep going to find the first empty space
                    have_jumped = True

        return valid
