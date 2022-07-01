from chess.coord import Coord
from chess.pieces.piece_base import PieceBase

blocked = [[Coord(-1, -2)], [Coord(-2, -1)],
           [Coord(1, -2)], [Coord(2, -1)],
           [Coord(-1, 2)], [Coord(-2, 1)],
           [Coord(1, 2)], [Coord(2, 1)]]


class Knight(PieceBase):
    name = 'knight'

    def block(self):
        return self.blocked
