from fastapi import HTTPException

from ss19.models.warehouse import Warehouse

def create_warehouse(data, db):
    try:
        warehouse = Warehouse(**data.model_dump())
        db.add(warehouse)
        db.commit()
        db.refresh(warehouse)
        return warehouse
    except Exception:
        db.rollback()
        raise

def get_warehouse_detail(warehouse_id: int,db):
    warehouse = (db.query(Warehouse).filter(Warehouse.id == warehouse_id).first())

    if not warehouse:
        raise HTTPException(
            status_code=404,
            detail="Warehouse not found"
        )
    
    return warehouse