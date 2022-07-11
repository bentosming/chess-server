import asyncio
import os

if os.name == 'nt':
    from asyncio.windows_events import ProactorEventLoop
from dataclasses import dataclass
from typing import Union

import pika
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from uvicorn import Config, Server

from chess_db import sa_tables
from chess_db.main import engine, SessionLocal
from chess_db.queries import get_task_by_n_and_piece, get_task

sa_tables.Base.metadata.create_all(bind=engine)
app = FastAPI()

if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ProactorServer(Server):
    def run(self, sockets=None):
        if os.name == 'nt':
            loop = ProactorEventLoop()
            asyncio.set_event_loop(loop)
        asyncio.run(self.serve(sockets=sockets))


@dataclass
class Task:
    id: int
    piece: str
    n: int
    placement_count: int = -1


@app.get("/")
async def root():
    return {"message": "Hello World"}


class ChessboardSettings(BaseModel):
    chessPiece: str
    n: int


app = FastAPI()


class PiecePlacementTaskBase(BaseModel):
    piece: str
    n: int


class PiecePlacementTaskId(BaseModel):
    id: int

    class Config:
        orm_mode = True


class PiecePlacementTaskCreate(PiecePlacementTaskBase):
    pass


class PiecePlacementTask(PiecePlacementTaskBase):
    id: int
    state: str
    solution: Union[None, int]

    class Config:
        orm_mode = True


def create_db_task(db: Session, task: PiecePlacementTaskCreate):
    db_task = sa_tables.PiecePlacementTask(n=task.n, piece=task.piece)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    print(db_task)
    return db_task


@app.post("/chessboard_piece_placer/", response_model=PiecePlacementTaskId)
def create_piece_placement_task(task: PiecePlacementTaskCreate, db: Session = Depends(get_db)):
    print(f"request to create {task}")
    db_task = get_task_by_n_and_piece(db, n=task.n, piece_type=task.piece)
    print(db_task)
    if db_task:
        raise HTTPException(status_code=400, detail="Task already registered")

    db_task = create_db_task(db=db, task=task)
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672))
    channel = connection.channel()

    channel.queue_declare(queue='piece_placer')

    channel.basic_publish(exchange='',
                          routing_key='piece_placer',
                          body=str(db_task.id))
    print(" [x] Sent 'Hello World!'")

    connection.close()
    return db_task


@app.get("/chessboard_piece_placer/{task_id}", response_model=PiecePlacementTask)
def read_user(task_id: int, db: Session = Depends(get_db)):
    db_task = get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


config = Config(app=app, reload=True, host="0.0.0.0")
server = ProactorServer(config=config)
server.run()
