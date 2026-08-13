
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()
class Product(Base):
    __tablename__ = "product"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(50),nullable=False)
    price =Column(Float,nullable=False)

