import abc
from typing import Iterable

from chess.coord import Coord

GENERATOR_LIMIT = 20


class PieceBase(abc.ABC):
    name: str

    def __init__(self, piece_id: int, min_valid_position: Coord):
        self.id = piece_id
        self.position = min_valid_position

    @abc.abstractmethod
    def block(self) -> Iterable[Iterable[Coord]]:
        pass

    def __repr__(self):
        return f"{self.name}{self.id} at {self.position}"
