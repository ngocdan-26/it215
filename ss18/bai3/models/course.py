from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ss18.src.database.base import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    max_students = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)

    enrollments = relationship(
        "Enrollment",
        back_populates="course"
    )