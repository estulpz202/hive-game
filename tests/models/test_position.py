from hive.models.position import Position


def test_position_equality():
    """Positions with same coordinates should be equal."""
    assert Position(0, 0) == Position(0, 0)
    assert Position(1, -1) != Position(0, 1)


def test_position_hashing():
    """Positions with same coordinates should have the same hash."""
    assert hash(Position(2, 3)) == hash(Position(2, 3))


def test_neighbors_returns_six_positions():
    """Position.neighbors() should return exactly six unique adjacent positions."""
    pos = Position(0, 0)
    neighbors = pos.neighbors()
    assert len(neighbors) == 6
    assert len(set(neighbors)) == 6  # Ensure all are unique


def test_neighbors_are_correct():
    """Ensure neighbors of (0, 0) match expected axial coordinates."""
    pos = Position(0, 0)
    expected = {
        Position(1, 0),
        Position(1, -1),
        Position(0, -1),
        Position(-1, 0),
        Position(-1, 1),
        Position(0, 1),
    }
    assert set(pos.neighbors()) == expected


def test_neighbors_are_cached():
    """Ensure neighbor results are reused via cache (indirectly)."""
    pos1 = Position(2, 2)
    pos2 = Position(2, 2)
    assert pos1.neighbors() is pos2.neighbors()
