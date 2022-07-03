from chess.coord import Coord
from chess.pieces.piece_base import PieceBase, GENERATOR_LIMIT

up = [Coord(-i, 0) for i in range(1, GENERATOR_LIMIT)]
down = [Coord(i, 0) for i in range(1, GENERATOR_LIMIT)]
left = [Coord(0, -i) for i in range(1, GENERATOR_LIMIT)]
right = [Coord(0, i) for i in range(1, GENERATOR_LIMIT)]
upleft = [Coord(-i, -i) for i in range(1, GENERATOR_LIMIT)]
downleft = [Coord(i, -i) for i in range(1, GENERATOR_LIMIT)]
upright = [Coord(-i, i) for i in range(1, GENERATOR_LIMIT)]
downright = [Coord(i, i) for i in range(1, GENERATOR_LIMIT)]


class Queen(PieceBase):
    name = "queen"

    def block(self):
        return [up, down, left, right, upleft, downleft, upright, downright]
