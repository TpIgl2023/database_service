

from sqlalchemy import Column, Integer, Sequence
from sqlalchemy.orm import relationship

from Database.database import Base, engine


class Favorite(Base):

    __tablename__ = "favorites"

    id = Column(Integer, Sequence("favorite_id_seq"), primary_key=True, index=True)


Base.metadata.create_all(bind=engine)
