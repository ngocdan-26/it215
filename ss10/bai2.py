# | STT | Phương thức truy vấn hiện tại | Tình huống gây lỗi (Edge Case)                                                                                                                   | Phương thức thay thế an toàn hơn                                                                             |
# | --- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
# | 1   | `.one()`                      | `order_id = 999` không tồn tại trong bảng `orders` → SQLAlchemy ném ngoại lệ `NoResultFound`, nếu không xử lý sẽ trả về lỗi 500 kèm Stack Trace. | `.first()` kết hợp kiểm tra `None` và chủ động trả về `HTTPException(status_code=status.HTTP_404_NOT_FOUND)` |

from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/connect_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    customer_name = Column(String(100))
    total_price = Column(Integer)

app = FastAPI()

@app.get("/orders/{order_id}")
def get_order_detail(order_id: int):
    db = SessionLocal()

    order = (
        db.query(OrderModel)
        .filter(OrderModel.id == order_id)
        .first()
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy đơn hàng"
        )

    return {
        "id": order.id,
        "customer": order.customer_name
    }