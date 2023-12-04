from sqlalchemy import Column, Integer
from database import Base, engine


class Moderator(Base):

    __tablename__ = "moderators"

    id = Column(Integer, primary_key=True, index=True)


Base.metadata.create_all(bind=engine)
