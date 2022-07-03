import asyncio
import os
import sys
from asyncio.windows_events import ProactorEventLoop
from dataclasses import dataclass

from fastapi import FastAPI
from pydantic import BaseModel
from uvicorn import Config, Server

app = FastAPI()
asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


class ProactorServer(Server):
    def run(self, sockets=None):
        loop = ProactorEventLoop()
        asyncio.set_event_loop(loop)  # since this is the default in Python 3.10, explicit selection can also be omitted
        asyncio.run(self.serve(sockets=sockets))


@dataclass
class Solution:
    piece: str
    n: int
    placement_count: int


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
    # Solution("queen", 6, 4),
    Solution("queen", 7, 40)
]


@app.get("/")
async def root():
    return {"message": "Hello World"}


# {“n”:4, “chessPiece”: “queen”}
class ChessboardSettings(BaseModel):
    chessPiece: str
    n: int


app = FastAPI()


@app.post("/chessboard_piece_placer/")
async def chessboard_settings(setting: ChessboardSettings):
    solution = [s for s in solutions if s.piece == setting.chessPiece and s.n == setting.n]
    if solution:
        print("Solution is ready")
        return solution
    print("Starting new process", setting)
    proc = await asyncio.create_subprocess_exec(sys.executable, os.path.abspath("../chess/piece_placer.py"),
                                                "-n", str(setting.n), "-p", f"{setting.chessPiece}",
                                                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()

    result = int(stdout.decode())
    print(stderr.decode())
    print("finishig process", setting)
    return Solution(setting.chessPiece, setting.n, result)


config = Config(app=app, reload=True)
server = ProactorServer(config=config)
server.run()
