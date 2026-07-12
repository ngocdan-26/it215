# | Tiêu chí                  | Giải pháp 1: Duyệt List | Giải pháp 2: Dùng Dict     |
# | ------------------------- | ----------------------- | -------------------------- |
# | Tốc độ tìm kiếm           | O(n)                    | O(1)                       |
# | Hiệu năng khi dữ liệu lớn | Chậm                    | Rất nhanh                  |
# | Bộ nhớ tiêu hao           | Thấp hơn                | Cao hơn một chút           |
# | Độ dễ hiểu                | Dễ                      | Dễ                         |
# | Khả năng bảo trì          | Trung bình              | Tốt                        |
# | Khả năng mở rộng          | Kém                     | Tốt                        |
# | Bối cảnh phù hợp          | Dữ liệu nhỏ             | Dữ liệu lớn, tra cứu nhiều |

from fastapi import FastAPI, HTTPException, status

app = FastAPI()

orders_dict = {
    1: {
        "code": "SP001",
        "payment_status": "PAID",
        "method": "BANK_TRANSFER"
    },
    2: {
        "code": "SP002",
        "payment_status": "UNPAID",
        "method": "NONE"
    }
}

@app.get("/orders/{order_id}/payment")
def get_payment_history(order_id: int):
    try:
        order = orders_dict.get(order_id)

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy đơn hàng"
            )

        return {
            "order_id": order_id,
            "payment_status": order["payment_status"],
            "method": order["method"]
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Đã xảy ra lỗi hệ thống, vui lòng thử lại sau"
        )