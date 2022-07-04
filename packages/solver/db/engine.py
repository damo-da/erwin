from sqlalchemy import create_engine
from os import environ
from sqlalchemy.orm import sessionmaker

db_url = environ.get("CHESS_DB_URL")
if not db_url:
    exit("Chess DB URL not provided.")

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
