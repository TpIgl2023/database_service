from sqlalchemy import Column, Integer
from Database.database import Base, engine


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)


Base.metadata.create_all(bind=engine)
