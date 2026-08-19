from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from ss19.database.database import get_db
from ss19.schema.warehouse import WarehouseCreate,WarehouseDetailResponse
from ss19.service.warehouse import create_warehouse,get_warehouse_detail
router_warehouse = APIRouter(
    prefix="/Warehouse",
    tags=["Warehouse"]
)

@router_warehouse.post("")
def add_warehouse(warehouse: WarehouseCreate,db: Session = Depends(get_db)):
    return create_warehouse(warehouse,db)


@router_warehouse.get("/{warehouse_id}",response_model=WarehouseDetailResponse)
def get_warehouse(
    warehouse_id: int,
    db: Session = Depends(get_db)
):
    return get_warehouse_detail(
        warehouse_id,
        db
    )
