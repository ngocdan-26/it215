from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ss18.bai4.database.base import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255))
    email = Column(String(255))
    status = Column(String(20))

    enrollments = relationship(
        "Enrollment",
        back_populates="student"
    )