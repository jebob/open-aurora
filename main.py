
class GamePiece:
    detectRange = 0  # by default things don't detect
    speed = 0  # by default things don't move
    """"This is a thing class. It represents an object or coll"""
    def __init__(self, position):
        assert isinstance(position, tuple)
        assert len(position) == 2
        assert all(isinstance(n, int) for n in position)
        self.position = position
