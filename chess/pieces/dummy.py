from chess.pieces.piece_base import PieceBase


class Dummy(PieceBase):
    name = "dummy"

    def block(self):
        return [[]]
