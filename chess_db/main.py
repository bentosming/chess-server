from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from chess_db.sa_tables import Base

engine = create_engine("postgresql://postgres:mysecretpassword@localhost:5432/postgres", echo=True)
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
