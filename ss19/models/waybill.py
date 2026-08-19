from ss19.database.base import Base
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship

class Waybill(Base):
    __tablename__ = "waybills"
    id = Column(Integer,primary_key=True,index=True)
    tracking_number = Column(String(100),nullable=False,unique=True)
    shipping_status = Column(String(100),nullable=False)
    package_id = Column(Integer,ForeignKey("packages.id"),nullable=False,unique=True)
    package = relationship("Package",back_populates="waybill")