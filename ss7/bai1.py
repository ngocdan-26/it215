from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Dữ liệu nội bộ trong bộ nhớ tạm - Chứa các trường nhạy cảm
orders_db = [
    {
        "id": 1,
        "customer_name": "Nguyen Van A",
        "total_amount": 1500000.0,
        "profit_margin": 0.25,      # Nhạy cảm - Cấm lộ!
        "supplier_id": "SUP_DELL_01" # Nhạy cảm - Cấm lộ!
    },
    {
        "id": 2,
        "customer_name": "Tran Thi B",
        "total_amount": 350000.0,
        "profit_margin": 0.30,       # Nhạy cảm - Cấm lộ!
        "supplier_id": "SUP_LOGI_02"  # Nhạy cảm - Cấm lộ!
    }
]

class OrderResponse(BaseModel):
    id: int
    customer_name: str
    total_amount: float

@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order_detail(order_id: int):
    for order in orders_db:
        if order["id"] == order_id:
            return {
                "id": order["id"],
                "customer_name": order["customer_name"],
                "total_amount": order["total_amount"]
            }

    raise HTTPException(
        status_code=404,
        detail="Order not found"
    )

# | STT | Dữ liệu gửi lên   | Kết quả hiện tại (Mã HTTP + Body)                                                                                                      | Kết quả đúng mong muốn                                                                | Lỗi phát hiện                                                                  |
# | --- | ----------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
# | 1   | `GET /orders/999` | **HTTP 200 OK**<br>`{"message":"Order not found"}`                                                                                     | **HTTP 404 Not Found**<br>`{"detail":"Order not found"}`                              | Trả về sai mã trạng thái HTTP. Không tìm thấy dữ liệu nhưng vẫn trả về 200 OK. |
# | 2   | `GET /orders/1`   | **HTTP 200 OK**<br>`{"id":1,"customer_name":"Nguyen Van A","total_amount":1500000.0,"profit_margin":0.25,"supplier_id":"SUP_DELL_01"}` | **HTTP 200 OK**<br>`{"id":1,"customer_name":"Nguyen Van A","total_amount":1500000.0}` | Lộ thông tin nhạy cảm `profit_margin` và `supplier_id`.                        |
