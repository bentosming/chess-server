import dataclasses


@dataclasses.dataclass(frozen=True)
class Coord:
    row: int
    column: int

    def __add__(self, other):
        return Coord(row=self.row + other.row, column=self.column + other.column)