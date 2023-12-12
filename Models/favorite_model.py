

from sqlalchemy import Column, Integer, Sequence, ForeignKey
from sqlalchemy.orm import relationship

from Database.database import Base, engine


class Favorite(Base):

    __tablename__ = "favorites"

    id = Column(Integer, Sequence("favorite_id_seq"), primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey('articles.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)


Base.metadata.create_all(bind=engine)
