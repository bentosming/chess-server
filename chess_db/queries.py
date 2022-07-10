from sqlalchemy.orm import Session

from chess_db import sa_tables
from chess_db.sa_tables import PiecePlacementTask


def get_task(db: Session, task_id: int) -> PiecePlacementTask:
    return db.query(sa_tables.PiecePlacementTask).filter(sa_tables.PiecePlacementTask.id == task_id).first()


def get_task_by_n_and_piece(db: Session, n: int, piece_type: str):
    return db.query(sa_tables.PiecePlacementTask).filter(
        (sa_tables.PiecePlacementTask.n == n) & (sa_tables.PiecePlacementTask.piece == piece_type)).first()