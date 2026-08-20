from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.base import Base


class Classroom(Base):
    __tablename__ = "classrooms"

    id = Column(Integer, primary_key=True, index=True)
    class_code = Column(String(50), unique=True, nullable=False)
    class_name = Column(String(100), nullable=False)
    max_students = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False)

    students = relationship(
        "Student",
        back_populates="classroom"
    )