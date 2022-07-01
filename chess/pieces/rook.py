from chess.coord import Coord
from chess.pieces.piece_base import GENERATOR_LIMIT, PieceBase


class Rook(PieceBase):
    name = 'rook'

    def block(self):
        up = (Coord(-i, 0) for i in range(1, GENERATOR_LIMIT))
        down = (Coord(i, 0) for i in range(1, GENERATOR_LIMIT))
        left = (Coord(0, -i) for i in range(1, GENERATOR_LIMIT))
        right = (Coord(0, i) for i in range(1, GENERATOR_LIMIT))
        return [up, down, left, right]