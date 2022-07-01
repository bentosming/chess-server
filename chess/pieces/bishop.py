from chess.pieces.piece_base import PieceBase, GENERATOR_LIMIT
from chess.coord import Coord


class Bishop(PieceBase):
    name = "bishop"

    def block(self):
        upleft = [Coord(-i, -i) for i in range(1, GENERATOR_LIMIT)]
        downleft = [Coord(i, -i) for i in range(1, GENERATOR_LIMIT)]
        upright = [Coord(-i, i) for i in range(1, GENERATOR_LIMIT)]
        downright = [Coord(i, i) for i in range(1, GENERATOR_LIMIT)]
        return [upleft, downleft, upright, downright]