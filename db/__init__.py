
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.config import DATABASE_URL, Base
from contextlib import asynccontextmanager

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
