import collections.abc
import dataclasses
import logging
from enum import Enum
from typing import Iterator, List, Generator

from chess.coord import Coord
from chess.pieces.piece_base import PieceBase

LOGGER = logging.getLogger(__name__)


class SquareStatusEnum(str, Enum):
    EMPTY = "E"
    OCC = "O"
    BLOCKED = "B"


@dataclasses.dataclass
class SquareStatus:
    status: SquareStatusEnum
    id: int

    def __repr__(self):
        return f"{self.status.value}{self.id}"


class ChessBoard(collections.abc.MutableMapping):
    def __setitem__(self, k: Coord, v: SquareStatus) -> None:
        if self.are_coords_valid(coord=k):
            self._board[k.row][k.column] = v

    def __delitem__(self, v: SquareStatus) -> None:
        raise NotImplementedError()

    def __getitem__(self, k: Coord) -> SquareStatus:
        if self.are_coords_valid(coord=k):
            return self._board[k.row][k.column]
        raise AttributeError()

    def __len__(self) -> int:
        return self._n * self._n

    def __iter__(self) -> Iterator[SquareStatus]:
        return (self[coord] for coord in self.iterate_squares(Coord(0, 0)))

    def __init__(self, n: int):
        self._board: List[List[SquareStatus]] = [[SquareStatus(SquareStatusEnum.EMPTY, 0) for _ in range(n)] for _ in
                                                 range(n)]
        self._n = n

    def pretty_print(self):
        if LOGGER.getEffectiveLevel() <= 30:
            return
        for row in self._board:
            print('   '.join([r.__repr__() for r in row]))
            print()

    def iterate_squares(self, start_position: Coord) -> Generator[Coord, None, None]:
        for r in range(start_position.row, self._n):
            if r == start_position.row:
                for c in range(start_position.column, self._n):
                    yield Coord(row=r, column=c)
            else:
                for c in range(self._n):
                    yield Coord(row=r, column=c)

    def are_coords_valid(self, coord: Coord):
        return 0 <= coord.row < self._n and 0 <= coord.column < self._n

    def place_piece(self, piece: PieceBase) -> List[Coord]:
        """
        changes state of board (occ for piece, blocked for relevant..)
        :param piece:
        :return: coords of squares that changed state from empty to something else
        """
        changed = []
        if self[piece.position].status != SquareStatusEnum.EMPTY:
            return []
        self[piece.position] = SquareStatus(id=piece.id, status=SquareStatusEnum.OCC)
        changed.append(piece.position)

        for direction in piece.block():
            for position in direction:
                coord = position + piece.position
                if not self.are_coords_valid(coord):
                    break
                if self[coord].status != SquareStatusEnum.EMPTY:
                    continue
                changed.append(coord)
                self[coord] = SquareStatus(SquareStatusEnum.BLOCKED, piece.id)
        return changed

    def next_square(self, coord: Coord):
        n = self._n
        if coord == Coord(n - 1, n - 1):
            return None
        if coord.column == n - 1:
            return Coord(coord.row + 1, 0)
        return Coord(coord.row, coord.column + 1)

    def undo(self, squares: List[Coord]):
        for coord in squares:
            LOGGER.debug(f"Undoing: {coord}")
            self[coord] = SquareStatus(SquareStatusEnum.EMPTY, 0)
            # self.pretty_print()
