from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/connect_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine
)

Base = declarative_base()

class InventoryModel(Base):
    __tablename__ = "inventories"
    id = Column(Integer, primary_key=True)
    warehouse_code = Column( String(50),unique=True, nullable=False)
    location = Column(String(100),nullable=False)

class InventoryCreate(BaseModel):
    warehouse_code: str = Field(
        min_length=1,
        max_length=50
    )
    location: str = Field(
        min_length=1,
        max_length=100
    )

app = FastAPI()

@app.post("/inventories")
def create_inventory(inventory: InventoryCreate):
    db = SessionLocal()

    try:
        existing_inventory = (
            db.query(InventoryModel).filter(InventoryModel.warehouse_code == inventory.warehouse_code).first())

        if existing_inventory:
            raise HTTPException(
                status_code=400,
                detail="Mã kho vận đã tồn tại trên hệ thống, không thể tạo trùng"
            )

        new_inventory = InventoryModel(
            warehouse_code=inventory.warehouse_code,
            location=inventory.location
        )

        db.add(new_inventory)
        db.commit()
        db.refresh(new_inventory)

        return {
            "message": "Tạo phiếu kho vận thành công",
            "data": {
                "id": new_inventory.id,
                "warehouse_code": new_inventory.warehouse_code,
                "location": new_inventory.location
            }
        }

    except HTTPException:
        raise

    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Đã xảy ra lỗi hệ thống, vui lòng thử lại sau"
        ) from exc

    finally:
        db.close()