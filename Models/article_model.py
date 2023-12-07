from sqlalchemy import Column, Integer, ForeignKey, Sequence
from sqlalchemy.orm import relationship

from Database.database import Base, engine


class Article(Base):

    __tablename__ = "articles"

    id = Column(Integer, Sequence("article_id_seq"), primary_key=True, index=True)




Base.metadata.create_all(bind=engine)
