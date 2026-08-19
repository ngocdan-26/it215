from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ss18.bai4.database.base import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    status = Column(String(20))

    enrollments = relationship(
        "Enrollment",
        back_populates="course"
    )