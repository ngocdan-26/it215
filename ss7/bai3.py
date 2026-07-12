from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

products_db = [
    {
        "id": 101,
        "name": "Bàn phím cơ",
        "stock": 5,
        "price": 1200000.0
    },
    {
        "id": 102,
        "name": "Chuột Gaming",
        "stock": 2,
        "price": 600000.0
    }
]

orders_db = []


class OrderCreate(BaseModel):
    product_id: int
    quantity: int


@app.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(order_request: OrderCreate):
    product = next(
        (
            product
            for product in products_db
            if product["id"] == order_request.product_id
        ),
        None
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sản phẩm không tồn tại"
        )

    if order_request.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Số lượng mua phải lớn hơn 0"
        )

    if order_request.quantity > product["stock"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sản phẩm không đủ số lượng trong kho"
        )

    product["stock"] -= order_request.quantity

    new_order = {
        "id": len(orders_db) + 1,
        "product_id": product["id"],
        "product_name": product["name"],
        "quantity": order_request.quantity,
        "unit_price": product["price"],
        "total_amount": product["price"] * order_request.quantity
    }

    orders_db.append(new_order)

    return {
        "message": "Tạo đơn hàng thành công",
        "data": new_order
    }


@app.get("/products")
def get_products():
    return products_db


@app.get("/orders")
def get_orders():
    return orders_db