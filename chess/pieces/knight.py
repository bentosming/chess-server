from chess.coord import Coord
from chess.pieces.piece_base import PieceBase


class Knight(PieceBase):
    name = 'knight'
    blocked = [[Coord(-1, -2)], [Coord(-2, -1)],
               [Coord(1, -2)], [Coord(2, -1)],
               [Coord(-1, 2)], [Coord(-2, 1)],
               [Coord(1, 2)], [Coord(2, 1)]]

    def block(self):
        return self.blocked
