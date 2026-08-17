from sqlalchemy import Column,Integer,DateTime,ForeignKey, text
from sqlalchemy.orm import relationship
from ss16.bai3.database.base import Base

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer,ForeignKey("students.id"),nullable=False)
    course_id = Column(Integer,ForeignKey("courses.id"),nullable=False)
    enrolled_at = Column(DateTime,server_default=text("CURRENT_TIMESTAMP"))
    student = relationship("Student",back_populates="enrollments")
    course = relationship("Course",back_populates="enrollments")
