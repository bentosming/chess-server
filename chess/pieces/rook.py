from chess.coord import Coord
from chess.pieces.piece_base import GENERATOR_LIMIT, PieceBase

up = (Coord(-i, 0) for i in range(1, GENERATOR_LIMIT))
down = (Coord(i, 0) for i in range(1, GENERATOR_LIMIT))
left = (Coord(0, -i) for i in range(1, GENERATOR_LIMIT))
right = (Coord(0, i) for i in range(1, GENERATOR_LIMIT))


class Rook(PieceBase):
    name = 'rook'

    def block(self):
        return [up, down, left, right]
