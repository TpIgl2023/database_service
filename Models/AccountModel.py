from sqlalchemy import Column, Integer, String, Sequence
from database import Base, engine


class Account(Base):

    __tablename__ = "accounts"

    id = Column(Integer, Sequence("account_id_seq"), primary_key=True, index=True)
    name = Column(String, index=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<User %r>' % self.name


Base.metadata.create_all(bind=engine)





