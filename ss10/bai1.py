# | STT | Hành vi lỗi trong code hiện tại                    | Hậu quả đối với Database MySQL                                                                                                                | Cách khắc phục bằng SQLAlchemy                                                                       |
# | --- | -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
# | 1   | Thiếu lệnh `db.commit()` sau `db.add(new_product)` | Dữ liệu chỉ tồn tại trong Session, không được ghi vĩnh viễn xuống bảng `products`. API trả về thành công nhưng database không có bản ghi mới. | Gọi `db.commit()` sau khi `db.add()` để xác nhận transaction và lưu dữ liệu vào MySQL.               |
# | 2   | Không giải phóng/đóng Session                      | Connection vẫn được giữ trong pool, lâu dài có thể gây rò rỉ kết nối, cạn kiệt connection pool và giảm hiệu năng hệ thống.                    | Sử dụng `try...finally` và gọi `db.close()` trong `finally` để luôn đóng Session sau khi xử lý xong. |

from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/connect_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    bind=engine
)

Base = declarative_base()

class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)

class ProductCreate(BaseModel):
    sku: str
    name: str
    price: float

app = FastAPI()

@app.post("/products")
def create_product(product: ProductCreate):
    db = SessionLocal()
    try:
        new_product = ProductModel(
            sku=product.sku,
            name=product.name,
            price=product.price
        )

        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return {
            "message": "Product created successfully",
            "data": {
                "id": new_product.id,
                "sku": new_product.sku,
                "name": new_product.name,
                "price": new_product.price
            }
        }
    finally:
        db.close()