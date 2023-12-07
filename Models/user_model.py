from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from Database.database import Base, engine


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, ForeignKey('accounts.id'), primary_key=True, index=True)

    account = relationship("Account", back_populates="user")


Base.metadata.create_all(bind=engine)
