from fastapi import FastAPI
app = FastAPI()
products = [
    {"id": 1, "name": "Laptop Dell", "price": 15000000},
    {"id": 2, "name": "Chuột Logitech", "price": 350000},
    {"id": 3, "name": "Bàn phím cơ", "price": 1200000}
]
# Vì route đang được khai báo là:
# @app.get("/products/product_id")
# FastAPI hiểu đây là đường dẫn cố định /products/product_id, không phải biến động.
# Path Parameter trong FastAPI phải đặt trong dấu {}.
# product_id chỉ là một chuỗi ký tự cố định trong URL, không phải biến nhận giá trị từ người dùng.
@app.get("/products/{product_id}")
def get_product_detail(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product

    return {"message": "Không tìm thấy sản phẩm"}