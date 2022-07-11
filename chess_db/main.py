import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from chess_db.sa_tables import Base
url = "postgresql://postgres:mysecretpassword@postgres:5432/postgres"
if os.name == 'nt':
    url = "postgresql://postgres:mysecretpassword@localhost:5432/postgres"
engine = create_engine(url, echo=True)
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
