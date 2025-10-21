import os

from sqlalchemy.orm import DeclarativeBase


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")

class Base(DeclarativeBase):
    pass