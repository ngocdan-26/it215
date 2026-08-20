from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.base import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )
    full_name = Column(String(100))
    phone = Column(String(20))
    address = Column(String(255))

    user = relationship(
        "User",
        back_populates="profile"
    )