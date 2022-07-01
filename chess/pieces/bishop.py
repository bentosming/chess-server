from chess.coord import Coord
from chess.pieces.piece_base import PieceBase, GENERATOR_LIMIT

upleft = [Coord(-i, -i) for i in range(1, GENERATOR_LIMIT)]
downleft = [Coord(i, -i) for i in range(1, GENERATOR_LIMIT)]
upright = [Coord(-i, i) for i in range(1, GENERATOR_LIMIT)]
downright = [Coord(i, i) for i in range(1, GENERATOR_LIMIT)]

BLOCKED = [upleft, downleft, upright, downright]


class Bishop(PieceBase):
    name = "bishop"

    def block(self):
        # upleft = [Coord(-i, -i) for i in range(1, GENERATOR_LIMIT)]
        # downleft = [Coord(i, -i) for i in range(1, GENERATOR_LIMIT)]
        # upright = [Coord(-i, i) for i in range(1, GENERATOR_LIMIT)]
        # downright = [Coord(i, i) for i in range(1, GENERATOR_LIMIT)]
        # return [upleft, downleft, upright, downright]
        return BLOCKED
