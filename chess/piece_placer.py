import logging
from typing import Type

from chess.chessboard import ChessBoard
from chess.coord import Coord
from chess.pieces.bishop import Bishop
from chess.pieces.dummy import Dummy
from chess.pieces.knight import Knight
from chess.pieces.piece_base import PieceBase
from chess.pieces.queen import Queen
from chess.pieces.rook import Rook

LOGGER = logging.getLogger(__name__)
logging.basicConfig()
LOGGER.setLevel('WARN')


class PiecePlacer:
    _piece_mapper = {"queen": Queen,
                     "rook": Rook,
                     "dummy": Dummy,
                     "bishop": Bishop,
                     "knight": Knight}

    def __init__(self, n: int, piece_type: str):
        self._piece_type: Type[PieceBase] = self._piece_mapper[piece_type]
        self._chessboard = ChessBoard(n)
        self._valid_placement_counter = 0
        self._n = n

    def find_placements(self):
        piece = self._piece_type(1, Coord(0, 0))
        self._place_piece(piece)
        return self._valid_placement_counter

    def _place_piece(self, piece: PieceBase):
        """
        iterates trough possible squares to place a piece, recursively places all the unplaces pieces.
        :param piece:
        :return: None
        """
        LOGGER.info(f"Placing piece: {piece}")
        for coord in self._chessboard.iterate_squares(piece.position):
            piece.position = coord
            to_undo = self._chessboard.place_piece(piece)
            if len(to_undo) == 0:
                continue

            # self.print_board()
            LOGGER.debug(f"To undo: {to_undo}")
            next_coord = self._chessboard.next_square(coord)
            next_piece = self._piece_type(piece.id + 1, next_coord)
            if next_piece.id > self._n:
                LOGGER.info(f"Placed all pieces: {piece}")
                self._valid_placement_counter += 1
                self.print_board()
                self._chessboard.undo(to_undo)
                continue

            if not next_piece.position:  # run out of space
                LOGGER.debug(f"Run out of space: {piece}")
                # self.print_board()
                self._chessboard.undo(to_undo)
                continue

            self._place_piece(next_piece)
            self._chessboard.undo(to_undo)

    def print_board(self):
        self._chessboard.pretty_print()
