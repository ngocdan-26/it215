from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.base import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    student_code = Column(
        String(50),
        unique=True,
        nullable=False
    )

    full_name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False
    )

    age = Column(Integer)

    gender = Column(String(20))

    class_id = Column(
        Integer,
        ForeignKey("classrooms.id")
    )

    classroom = relationship(
        "Classroom",
        back_populates="students"
    )

    enrollments = relationship(
        "Enrollment",
        back_populates="student"
    )