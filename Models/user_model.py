from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from Database.database import Base, engine


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, ForeignKey('accounts.id'), primary_key=True, index=True)

    account = relationship("Account", back_populates="user")
    favorite_articles = relationship(
        "Article",
        secondary="favorites",
        back_populates="favorite_by",
    )


Base.metadata.create_all(bind=engine)
