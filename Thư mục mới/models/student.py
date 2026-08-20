from sqlalchemy import Column, ForeignKey, Integer, String
from database.base import Base

class Students(Base):
    __tablename__ = "students"
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    student_code = Column(String(100),nullable=False,unique=False)
    full_name = Column(String(100),nullable=False)
    email = Column(String(100),nullable=False)
    class_id = Column(Integer,ForeignKey("Classrooms.id"))
    # classroom = relationship("Classrooms" ,back_populates="student")
