from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ss18.src.database.database import get_db
from ss18.src.schema.product import CreateProduct
from ss18.src.services.product import add_new_product, delete_product_by_id, get_product, get_product_detail, update_product_by_id

pro_router = APIRouter(
    prefix="/product",
    tags=["product"]
    )

@pro_router.get("")
def get_all_product(db:Session=Depends(get_db)):
    return get_product(db)

@pro_router.get("/{pro_id}")
def get_product_by_id(pro_id:int,db:Session=Depends(get_db)):
    return get_product_detail(pro_id,db)

@pro_router.post("")
def add_product(product:CreateProduct,db:Session=Depends(get_db)):
    return add_new_product(product,db)

@pro_router.put("/{pro_id}")
def update_product(product:CreateProduct,pro_id:int,db:Session=Depends(get_db)):
    return update_product_by_id(product,pro_id,db)

@pro_router.delete("/{pro_id}")
def delete_product(pro_id:int,db:Session=Depends(get_db)):
    return delete_product_by_id(pro_id,db)