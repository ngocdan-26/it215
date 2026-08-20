from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.base import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)

    course_code = Column(
        String(50),
        unique=True,
        nullable=False
    )

    course_name = Column(
        String(100),
        nullable=False
    )

    credits = Column(
        Integer,
        nullable=False
    )

    enrollments = relationship(
        "Enrollment",
        back_populates="course"
    )