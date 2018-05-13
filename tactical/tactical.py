from tactical.pieces import GamePiece


class Tactical:
    """This is the tactical view"""
    def __init__(self):
        self.pieceList = []

    def test_render(self):
        """This is a demo configuration"""
        demo_posns = [1+2j, 4+5j, 3-1j]
        self.pieceList = [GamePiece(posn, 0.0) for posn in demo_posns]

    def test_paint_performance(self):
        """This is a demo configuration"""
        demo_posns = [random.randrange(0, 400) + random.randrange(0, 400)*1j for _ in range(100000)]
        self.pieceList = [GamePiece(posn, 0.0) for posn in demo_posns]

