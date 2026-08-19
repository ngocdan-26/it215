
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ss18.src.database.database import get_db
from ss18.src.schema.category import CreateCategory
from ss18.src.services.category import add_new_category, delete_category_by_id, get_category, update_category_by_id


cat_router = APIRouter(
    prefix="/category",
    tags=["Category"]
)

@cat_router.get("")
def get_all_category(db:Session = Depends(get_db)):
    return get_category(db)

@cat_router.post("")
def add_category(category:CreateCategory,db:Session = Depends(get_db)):
    return add_new_category(category,db)

@cat_router.put("/{cat_id}")
def update_category(category:CreateCategory,cat_id:int,db:Session=Depends(get_db)):
    return update_category_by_id(category,cat_id,db)

@cat_router.delete("/{cat_id}")
def delete_category(cat_id:int, db:Session=Depends(get_db)):
    return delete_category_by_id(cat_id,db)