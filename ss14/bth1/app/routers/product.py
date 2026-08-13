from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from ss14.bth1.app.database.database import get_db
from ss14.bth1.app.schema.product import productCreat 
from ss14.bth1.app.services.product import get_product,get_product_by_id,add_new_product,update_product_by_id,delete_product_by_id
router = APIRouter(
    prefix="/Products",
    tags=["Products"]
)

@router.get("")
def get_all_product(db:Session = Depends(get_db)):
    return get_product(db)

@router.get("/{pro_id}")
def get_product_detail(pro_id:int,db:Session=Depends(get_db)):
    return get_product_by_id(pro_id,db)

@router.post("")
def add_product(product:productCreat,db:Session=Depends(get_db)):
    return add_new_product(product,db)

@router.put("/{pro_id}")
def update_product(product:productCreat,pro_id:int,db:Session=Depends(get_db)):
    return update_product_by_id(product,pro_id,db)

@router.delete("/{pro_id}")
def delete_product(pro_id:int,db:Session=Depends(get_db)):
    return delete_product_by_id(pro_id,db)