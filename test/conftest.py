from sqlalchemy import create_engine
from solver.db import Base, GameResult
from sqlalchemy.orm import sessionmaker

import pytest


@pytest.fixture(scope="session")
def db_sess():
    engine = create_engine("postgresql://damodaha@localhost/chess")
    Base.metadata.create_all(engine)

    Session = sessionmaker()
    Session.configure(bind=engine)

    session = Session()

    yield session

    session.close()
