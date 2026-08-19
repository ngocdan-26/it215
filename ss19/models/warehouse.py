from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import relationship
from ss19.database.base import Base

class Warehouse(Base):
    __tablename__ = "warehouses"
    id = Column(Integer,primary_key=True,index=True)
    warehouse_name = Column(String(255),nullable=False)
    location = Column(String(255),nullable=False)
    packages = relationship("Package",back_populates="warehouse")

