from sqlalchemy import (Column,Integer,String)
from sqlalchemy.orm import relationship
from ss16.bai3.database.base import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100),unique=True,nullable=False)
    max_students = Column(Integer,nullable=False)
    enrollments = relationship("Enrollment",back_populates="course")
    students = relationship("Student",secondary="enrollments",back_populates="courses",viewonly=True)