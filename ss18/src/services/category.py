from fastapi import HTTPException

from ss18.src.models.category import Category
from ss18.src.models.product import Product


def get_category(db):
    category = db.query(Category).all()
    return{
        "message":"lay danh sach danh muc",
        "data":category
    }

def add_new_category(category,db):
    new_category = Category(
        cat_name = category.cat_name
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return{
        "message":"them danh muc thanh cong",
        "data":new_category
    }

def update_category_by_id(update_category,cat_id:int,db):
    category = db.query(Category).filter(cat_id == Category.id).first()
    if not category:
        raise HTTPException(
            status_code=404,
            detail="khong tim thay danh muc"
        )
    existing_category = db.query(Category).filter(Category.cat_name == category.cat_name,Category.id != cat_id).first()
    if existing_category:
        raise HTTPException(
            status_code=400,
            detail="Tên danh mục đã tồn tại"
        )
    cat_check = db.query(Category).filter(cat_id == Product.cat_id).first()
    if cat_check:
        raise HTTPException(
            status_code=400,
            detail="co danh muc chua san pham"
        )
    category.cat_name = update_category.cat_name
    db.commit()
    db.refresh(category)
    return{
        "message":"sua danh muc thanh cong",
        "data": category
    }

def delete_category_by_id(cat_id,db):
    category = db.query(Category).filter(Category.id == cat_id).first()
    if category is None:
        raise HTTPException(
            status_code=404,
            detail="khong tim thay danh muc"
        )
    cat_check = db.query(Category).filter(cat_id == Product.cat_id).first()
    if cat_check:
        raise HTTPException(
            status_code=400,
            detail="co danh muc chua san pham"
        )
    db.delete(category)
    db.commit()
    return{
        "message":"xoa san pham thanh cong",
        "data" : category
    }