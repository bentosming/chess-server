from sqlalchemy import Column, Integer, String, UniqueConstraint

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class PiecePlacementTask(Base):
    __tablename__ = 'piece_placement_task'
    id = Column(Integer, primary_key=True)
    piece = Column(String, nullable=False)
    n = Column(Integer, nullable=False)
    solution = Column(Integer, nullable=True)
    state = Column(String, nullable=False, default="Unprocessed")
    __table_args__ = (UniqueConstraint('piece', 'n', name='_piece_placement_task_uc'),
                      )

    def __repr__(self):
        return "<PiecePlacementTask(piece_type='%s', n='%i', solution='%s')>" % (
            self.piece, self.n, self.solution)
