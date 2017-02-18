
class GamePiece:
    """"This is the parent of all classes that have a presence on the map."""
    detectRange = 0  # by default things don't detect
    speed = 0  # by default things don't move

    def __init__(self, position):
        assert isinstance(position, tuple)
        assert len(position) == 2
        assert all(isinstance(n, int) for n in position)
        self.position = position
