from sqlalchemy import Column, Integer, String, Float
from ss14.bth1.app.database.base import Base

class Product(Base):    
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)