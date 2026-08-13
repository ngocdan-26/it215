from sqlalchemy import Column, Float, Integer, String

from ss14.bth2.app.database.base import Base


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    full_name = Column(String(100),nullable=False)
    email = Column(String(100),nullable=False)
    major = Column(String(100),nullable=False)
    gpa = Column(Float,nullable=False)
