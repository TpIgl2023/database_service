from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import relationship

from Database.database import Base, engine


class Account(Base):

    __tablename__ = "accounts"

    id = Column(Integer, Sequence("account_id_seq"), primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    password = Column(String, index=True)
    phone = Column(String, index=True)

    user = relationship("User", back_populates="account", cascade="all, delete-orphan")
    moderator = relationship("Moderator", back_populates="account", cascade="all, delete-orphan")
    administrator = relationship("Administrator", back_populates="account", cascade="all, delete-orphan")

    @staticmethod
    def from_dict(dictionary):
        return Account(
            name=dictionary["name"],
            email=dictionary["email"],
            password=dictionary["password"],
            phone=dictionary["phone"]
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "phone": self.phone
        }


Base.metadata.create_all(bind=engine)





