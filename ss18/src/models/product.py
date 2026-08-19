from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ss18.src.database.base import Base


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    pro_name = Column(String(100),nullable=False)
    price = Column(Float)
    cat_id = Column(Integer,ForeignKey("category.id"))
    category = relationship("Category",back_populates="products")
