from sqlalchemy import create_engine
from solver.db import Base, GameResult
from sqlalchemy.orm import sessionmaker
from os import getenv
import pytest


@pytest.fixture(scope="session")
def db_sess():
    db_url = getenv("CHESS_DB_URL")
    engine = create_engine(db_url)

    Session = sessionmaker()
    Session.configure(bind=engine)

    session = Session()

    yield session

    session.close()
