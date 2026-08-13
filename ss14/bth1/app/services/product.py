from fastapi import HTTPException

from ss14.bth1.app.models.product import Product

def get_product(db):
    product= db.query(Product).all()
    return{
        "message":"lay dand sach thnah cong",
        "data": product
    }

def get_product_by_id(pro_id:int,db):
    product= db.query(Product).filter(Product.id == pro_id).first()
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="khong tim thay san pham"
        )
    return{
        "message":"tim thay san pham",
        "data": product
    }

def add_new_product(product,db):
    new_product = Product(
        name = product.name,
        price = product.price
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return{
        "message":"them sinh vien thanh cong",
        "data": new_product
    }

def update_product_by_id(update_product,pro_id,db):
    product = db.query(Product).filter(Product.id == pro_id).first()
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="khong tim thay san pham"
        )
    product.name = update_product.name
    product.price = update_product.price
    db.commit()
    db.refresh(product)
    return{
        "message":"cap nhat san pham thanh cong",
        "data":product
    }

def delete_product_by_id(pro_id:int,db):
    product= db.query(Product).filter(Product.id == pro_id).first()
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="san pham khong ton tai"
        )
    db.delete(product)
    db.commit()
    return{
        "message":"xoa san pham thanh cong",
        "data":product
    }