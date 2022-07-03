import pytest as pytest

from chess.piece_placer import PiecePlacer


@pytest.mark.parametrize(
    ['piece', 'n', 'expected'],
    [("dummy", 1, 1),
     ("dummy", 2, 6),
     ("dummy", 5, 53130),
     ("rook", 1, 1),
     ("rook", 2, 2),
     ("rook", 3, 3 * 2),
     ("rook", 5, 5 * 4 * 3 * 2),
     ("queen", 1, 1),
     ("queen", 2, 0),
     ("queen", 3, 0),
     ("queen", 4, 2),
     ("queen", 5, 10),
     # ("queen", 6, 4),
     # ("queen", 7, 40),
     # ("queen", 8, 92),
     # ("queen", 9, 352),
     ("bishop", 1, 1),
     ("bishop", 2, 4),
     ("knight", 1, 1),
     ("knight", 2, 6),
     ]
)
def test_find_placements(piece, n, expected):
    assert PiecePlacer(n, piece).find_placements() == expected
