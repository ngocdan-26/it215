from sqlalchemy import Column, Integer, String
from database.base import Base


class Classrooms(Base):
    __tablename__ = "classrooms"
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    class_code = Column(String(100),unique=False,nullable=False)
    class_name = Column(String(100),unique=False,nullable=False)
    # student = relationship("Students",back_populates="classroom")
