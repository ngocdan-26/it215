from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel

DATABASE_URL = "mysql+pymysql://root:12345d@localhost:3306/py_session10"

engine = create_engine(DATABASE_URL)
app = FastAPI()

SessionLocal = sessionmaker(
    bind=engine
)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ShipmentModel(Base):
    __tablename__ = "shipments"
    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String(50), unique=True, nullable=False)
    status = Column(String(50), default="PREPARING")

class ShipmentCreate(BaseModel):
    tracking_number: str

@app.get("/shipments", status_code=status.HTTP_200_OK)
def get_shipments(db: Session = Depends(get_db)):
    shipments = db.query(ShipmentModel).all()
    return {
        "message": "Danh sach van don",
        "data": shipments
    }

@app.post("/shipments", status_code=status.HTTP_201_CREATED)
def add_shipment(shipment: ShipmentCreate, db: Session = Depends(get_db)):
    existed_shipment = db.query(ShipmentModel).filter(ShipmentModel.tracking_number == shipment.tracking_number).first()
    if existed_shipment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mã vận đơn này đã được khởi tạo trước đó"
        )

    new_shipment = ShipmentModel(tracking_number=shipment.tracking_number)

    db.add(new_shipment)
    db.commit()
    db.refresh(new_shipment)
    return {
        "message": "Them van don thanh cong",
        "data": new_shipment
    }