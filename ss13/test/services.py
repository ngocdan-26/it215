from fastapi import HTTPException
from ss13.test.models import Product
from ss13.test.schema import ProductCreate


def get_all_product(db):
    return db.query(Product).all()

def get_product_detail(pro_id:int, db):
    product = db.query(Product).filter(Product.id == pro_id).fist()
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="khong tim thay"
        )
    return{
        "message":"tim thay san pham",
        "data":product
    }

def add_new_product(product:ProductCreate,db):
    new_product = Product(
        name=product.name,
        price=product.price
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return{
        "message":"them sp thanh cong",
        "data": new_product
    }

def delete_by_product(pro_id:int,db):
    product = db.query(Product).filter(Product.id == pro_id).first()
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="khong tim thay"
        )
    db.delete(product)
    db.commit()
    return{
        "meesage":"xoa san pham thanh cong",
        "data":product
    }

def update_by_id(pro_id:int,update_product:ProductCreate,db):
    product = db.query(Product).filter(Product.id == pro_id).first()
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="khong tim thay"
        )
    product.name = update_product.name
    product.price = update_product.price
    return{
        "message":"thay doi thanh cong",
        "data": product
    }
