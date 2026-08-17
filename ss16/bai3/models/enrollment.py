from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ss16.bai3.database.base import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100),nullable=False)
    status = Column(String(20),default="ACTIVE")
    enrollments = relationship("Enrollment",back_populates="student")
    courses = relationship("Course",secondary="enrollments",back_populates="students",viewonly=True)