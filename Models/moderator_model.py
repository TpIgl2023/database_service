from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from Database.database import Base, engine


class Moderator(Base):

    __tablename__ = "moderators"

    id = Column(Integer, ForeignKey('accounts.id'), primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey('administrators.id'), index=True)

    account = relationship("Account", back_populates="moderator")


Base.metadata.create_all(bind=engine)
