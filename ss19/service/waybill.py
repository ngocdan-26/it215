from fastapi import HTTPException
from ss19.models.waybill import Waybill

def delete_waybill(
    waybill_id: int,db):
    waybill = db.query(Waybill).filter(Waybill.id == waybill_id).first()
    if not waybill:
        raise HTTPException(
            status_code=404,
            detail="Waybill not found"
        )
    try:
        db.delete(waybill)
        db.commit()
        return {
            "message": "Delete successfully"
        }
    except Exception:
        db.rollback()
        raise