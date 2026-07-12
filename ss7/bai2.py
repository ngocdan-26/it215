# | STT | Dữ liệu/Endpoint gửi lên                             | Kết quả hiện tại (Mã HTTP + Body)                                                   | Kết quả đúng mong muốn                                             | Lỗi phát hiện                                                                                                                                             |
# | --- | ---------------------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
# | 1   | `PUT /orders/999/status` với `{"status":"SHIPPING"}` | **HTTP 200 OK**<br>`{"statusCode":200,"message":"Cập nhật thành công","data":null}` | **HTTP 404 Not Found**<br>`{"detail":"Order not found"}`           | Không xử lý lỗi đúng chuẩn. Chỉ `print("Order not found!")` nhưng không dừng chương trình bằng `raise HTTPException(404)`, nên API vẫn trả về thành công. |
# | 2   | `PUT /orders/1/status` với `{"status":"TRONG_SANG"}` | **HTTP 200 OK**<br>`{"error":"Trạng thái không hợp lệ"}`                            | **HTTP 400 Bad Request**<br>`{"detail":"Trạng thái không hợp lệ"}` | Sai chuẩn RESTful. Trạng thái không hợp lệ nhưng vẫn trả về HTTP 200 thay vì 400 Bad Request.                                                             |


from enum import Enum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

orders_db = [
    {"id": 1, "customer_name": "Nguyen Van A", "status": "PENDING"},
    {"id": 2, "customer_name": "Tran Thi B", "status": "SHIPPING"}
]

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    SHIPPING = "SHIPPING"
    DELIVERED = "DELIVERED"

class StatusUpdate(BaseModel):
    status: OrderStatus

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    order = next((o for o in orders_db if o["id"] == order_id), None)
    if order is None:
        raise HTTPException(status_code=404,
            detail="Order not found"
        )
    return order

@app.put("/orders/{order_id}/status")
def update_order_status(order_id: int, data: StatusUpdate):
    order = next((o for o in orders_db if o["id"] == order_id), None)
    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )
    order["status"] = data.status.value
    return {
        "message": "Cập nhật thành công",
        "data": order
    }