from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import create_engine, Column,Integer, String,Boolean
from sqlalchemy.orm import sessionmaker, Session,declarative_base
from pydantic import BaseModel

DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/connect_db"
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

class ParkingSlot(Base):
    __tablename__ = "parking_slots"

    id = Column(Integer, primary_key=True, index=True)
    slot_code = Column(String(50), unique=True, nullable=False)
    zone_name = Column(String(255), nullable=False)
    max_weight = Column(Integer, nullable=False)
    is_available = Column(Boolean, nullable=False, default=True)

class ParkingSlotCreate(BaseModel):
    slot_code :str
    zone_name:str
    max_weight:str

@app.post("/parking-slots")
def add_parking_slot(zone: ParkingSlotCreate,db: Session = Depends(get_db)):
    new_slot = ParkingSlot(
        slot_code=zone.slot_code,
        zone_name=zone.zone_name,
        max_weight=zone.max_weight
    )

    db.add(new_slot)
    db.commit()
    db.refresh(new_slot)
    return{
        "statusCode": 201,
        "message": "Thêm vị trí đỗ xe thành công",
        "error": None,
        "data": new_slot,
        "timestamp": "2026-07-01T15:20:00Z"
    }

@app.get("/parking-slots")
def get_all_parkingslot(db:Session = Depends(get_db)):
    parkingslot = db.query(ParkingSlot).all()

    if parkingslot is None:
        raise HTTPException(
            status_code=404,
            detail="Parking slot not found"
        )

    return {
        "data": parkingslot
    }

@app.get("/parking-slots/{slot_id}")
def get_parking_detail(slot_id: int,db: Session = Depends(get_db)):
    parkingslot = (db.query(ParkingSlot).filter(ParkingSlot.id == slot_id).first())

    if parkingslot is None:
        raise HTTPException(
            status_code=404,
            detail="Parking slot not found"
        )

    return {
        "message": "Lấy vị trí đỗ xe thành công",
        "data": parkingslot
    }