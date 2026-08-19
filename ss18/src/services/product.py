from fastapi import HTTPException

from ss18.src.models.category import Category
from ss18.src.models.product import Product


def get_product(db):
    product = db.query(Product).all()
    return {
        "message":"lay danh sach san pham",
        "data":product
    }

def get_product_detail(pro_id,db):
    product = db.query(Product).filter(Product.id == pro_id).first()
    
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="san pham khong ton tai"
        ) 
    return{
        "message":"tim thay san pham",
        "data":product
    }

def add_new_product(product,db):
    category = db.query(Category).filter(Category.id == product.cat_id).first()
    if not category:
        raise HTTPException(
            status_code=404,
            detail="Danh mục không tồn tại"
        )
    
    new_product = Product(
        pro_name = product.pro_name,
        price = product.price,
        cat_id = product.cat_id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return{
        "message":"them san pham thanh cong",
        "data" : new_product
    }

def update_product_by_id(update_product,pro_id,db):
    product = db.query(Product).filter(Product.id == pro_id).first()
    if not product:
        raise HTTPException(
            status_code=404,
            detail="khong tim thay sn pham"
        )
    category = db.query(Category).filter(Category.id == update_product.cat_id).first()
    if not category:
        raise HTTPException(
            status_code=404,
            detail="khong ton tai danh muc"
        )
    product.pro_name = update_product.pro_name
    product.price = update_product.price
    product.cat_id = update_product.cat_id
    db.commit()
    db.refresh(product)
    return{
        "message":"cap nhat san pham thanh cong",
        "data":product
    }

def delete_product_by_id(pro_id,db):
    product = db.query(Product).filter(Product.id == pro_id).first()
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="khong tim thay san pham"
        )
    db.delete(product)
    db.commit()
    return{
        "message":"xoa san pham thanh cong",
        "data": product
    }