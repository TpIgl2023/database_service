from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

_SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(_SQLALCHEMY_DATABASE_URL)
_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db() -> Session:
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()
