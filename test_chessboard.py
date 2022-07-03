import time
from dataclasses import dataclass

from chess.piece_placer import PiecePlacer
from server.main import Solution

solutions = [
        Solution("dummy", 1, 1),
        Solution("dummy", 2, 6),
        Solution("dummy", 5, 53130),
        Solution("rook", 1, 1),
        Solution("rook", 2, 2),
        Solution("rook", 3, 3 * 2),
        Solution("rook", 5, 5 * 4 * 3 * 2),
        Solution("queen", 1, 1),
        Solution("queen", 2, 0),
        Solution("queen", 3, 0),
        Solution("queen", 4, 2),
        Solution("queen", 5, 10),
        Solution("queen", 6, 4),
    #     Solution("queen", 7, 40),
    #     # Solution("queen", 8, 92),
    #     # Solution("queen", 9, 352),
    # Solution("bishop", 1, 1),
    # Solution("bishop", 2, 4),
    #     Solution("knight", 1, 1),
    #     Solution("knight", 2, 6),
    #
]
# #
# for s in solutions:
#     print(s)
#     assert PiecePlacer(s.n, s.piece).find_placements() == s.placement_count
#
# placer3 = PiecePlacer(3, "dummy")
# board3 = placer3._chessboard
#
# assert board3.next_square(Coord(0, 0)) == Coord(0, 1)
# assert board3.next_square(Coord(0, 1)) == Coord(0, 2)
# assert board3.next_square(Coord(0, 2)) == Coord(1, 0)
# assert board3.next_square(Coord(2, 2)) is None
t = time.time()
print(time.time())
all_solutions = []
for piece in ["knight"]:
    # if piece == 'dummy':
    #     continue
    for i in range(1, 8):
        placements = PiecePlacer(i, piece).find_placements()
        all_solutions.append(Solution(piece, i, placements))
        print(f"{piece} {i}: {placements}")
        print(time.time()-t)
        print(all_solutions)

print(time.time()-t)
#bishop range(1,7): 6.1
#bishop range(1,8): 117, pak 94
# knight 7: 8891854 # 373.5010368824005