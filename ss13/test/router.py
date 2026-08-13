from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from ss13.test.database import get_db
from ss13.test.schema import ProductCreate
from ss13.test.services import add_new_product, delete_by_product, get_all_product, get_product_detail, update_by_id

router = APIRouter(
    prefix="/products",
    tags=["Product"]
)

@router.get("")
def get_product(db:Session = Depends(get_db)):
    return{
        "data":get_all_product(db)
    }
@router.get("/{productid}")
def get_product_by_id(product_id:int,db:Session = Depends(get_db)):
    return get_product_detail(product_id,db)

@router.post("")
def add_product(product:ProductCreate, db:Session =Depends(get_db)):
    return add_new_product(product,db)

@router.delete("/{product_id}")
def delete_product(product_id:int,db:Session= Depends(get_db)):
    return delete_by_product(product_id,db)

@router.put("/{product_id}")
def update_product(product_id,product:ProductCreate,db:Session = Depends(get_db)):
    return update_by_id(product_id,product,db)