from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ss18.src.database.base import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False)

    enrollments = relationship(
        "Enrollment",
        back_populates="student"
    )