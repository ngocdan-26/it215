from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from ss19.database.database import get_db
from ss19.service.waybill import delete_waybill

router_waybill = APIRouter(
    prefix="/Waybill",
    tags=["Waybill"]
)

@router_waybill.delete("/{waybill_id}")
def remove_waybill(waybill_id: int,db: Session = Depends(get_db)):
    return delete_waybill(waybill_id,db)