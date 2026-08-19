from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ss18.src.database.base import Base


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    cat_name = Column(String(100),nullable=False,unique=False)
    products = relationship("Product",back_populates="category")
