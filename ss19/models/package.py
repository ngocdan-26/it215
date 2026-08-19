from sqlalchemy import Column,Integer,String,Float,ForeignKey
from sqlalchemy.orm import relationship
from ss19.database.base import Base


class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer,primary_key=True,index=True)
    package_code = Column(String(100),nullable=False,unique=True)
    weight = Column(Float,nullable=False)
    warehouse_id = Column(Integer,ForeignKey("warehouses.id"),nullable=False)
    warehouse = relationship("Warehouse",back_populates="packages")
    waybill = relationship("Waybill",back_populates="package",selist=False)