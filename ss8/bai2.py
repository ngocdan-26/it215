from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Literal
import re

app = FastAPI()

assets = [
    {"id": 1, "serial_number": "SN-MAC-01", "model": "MacBook Pro M3", "stock_available": 5, "status": "READY"},
    {"id": 2, "serial_number": "SN-DELL-02", "model": "Dell UltraSharp 27", "stock_available": 10, "status": "READY"},
    {"id": 3, "serial_number": "SN-THINK-03", "model": "ThinkPad X1 Carbon", "stock_available": 0, "status": "REPAIRING"}
]

allocations = [
    {
        "id": 1,
        "asset_id": 1,
        "employee_email": "dev.nguyen@company.com",
        "allocated_quantity": 1,
        "start_date": "2026-07-01",
        "duration_months": 12
    }
]


class AssetRequest(BaseModel):
    serial_number: str
    model: str = Field(min_length=2, max_length=255)
    stock_available: int = Field(ge=0)
    status: Literal["READY", "ALLOCATED", "REPAIRING", "SCRAPPED"]


class AllocationRequest(BaseModel):
    asset_id: int
    employee_email: str
    allocated_quantity: int = Field(gt=0)
    start_date: str
    duration_months: int = Field(ge=1, le=12)


@app.post("/assets")
def create_asset(asset_request: AssetRequest):
    asset_request = asset_request.model_dump()

    for asset in assets:
        if asset["serial_number"] == asset_request["serial_number"]:
            raise HTTPException(
                status_code=400,
                detail="Serial number already exists"
            )

    new_asset = {
        "id": len(assets) + 1,
        **asset_request
    }

    assets.append(new_asset)

    return {
        "message": "Thêm tài sản thành công",
        "data": new_asset
    }


@app.get("/assets")
def get_assets(
    keyword: Optional[str] = None,
    status: Optional[str] = None,
    min_stock: Optional[int] = None
):
    result = assets

    if keyword:
        result = [
            asset for asset in result
            if keyword.lower() in asset["serial_number"].lower()
            or keyword.lower() in asset["model"].lower()
        ]

    if status:
        result = [
            asset for asset in result
            if asset["status"] == status
        ]

    if min_stock is not None:
        result = [
            asset for asset in result
            if asset["stock_available"] >= min_stock
        ]

    return result


@app.get("/assets/{asset_id}")
def get_asset(asset_id: int):
    for asset in assets:
        if asset["id"] == asset_id:
            return asset

    raise HTTPException(
        status_code=404,
        detail="Asset not found"
    )


@app.put("/assets/{asset_id}")
def update_asset(asset_id: int, asset_request: AssetRequest):
    asset_request = asset_request.model_dump()

    for asset in assets:
        if (
            asset["serial_number"] == asset_request["serial_number"]
            and asset["id"] != asset_id
        ):
            raise HTTPException(
                status_code=400,
                detail="Serial number already exists"
            )

    for asset in assets:
        if asset["id"] == asset_id:
            asset.update(asset_request)

            return {
                "message": "Cập nhật thành công",
                "data": asset
            }

    raise HTTPException(
        status_code=404,
        detail="Asset not found"
    )


@app.delete("/assets/{asset_id}")
def delete_asset(asset_id: int):
    for asset in assets:
        if asset["id"] == asset_id:
            assets.remove(asset)

            return {
                "message": "Xóa thành công"
            }

    raise HTTPException(
        status_code=404,
        detail="Asset not found"
    )


@app.post("/allocations")
def create_allocation(allocation_request: AllocationRequest):
    allocation_request = allocation_request.model_dump()

    asset = None

    for item in assets:
        if item["id"] == allocation_request["asset_id"]:
            asset = item
            break

    if asset is None:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    if asset["status"] != "READY":
        raise HTTPException(
            status_code=400,
            detail="Asset is not ready"
        )

    if allocation_request["allocated_quantity"] > asset["stock_available"]:
        raise HTTPException(
            status_code=400,
            detail="Not enough stock available"
        )

    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if not re.match(email_pattern, allocation_request["employee_email"]):
        raise HTTPException(
            status_code=400,
            detail="Invalid email format"
        )

    asset["stock_available"] -= allocation_request["allocated_quantity"]

    new_allocation = {
        "id": len(allocations) + 1,
        **allocation_request
    }

    allocations.append(new_allocation)

    return {
        "message": "Cấp phát thiết bị thành công",
        "data": new_allocation
    }


@app.get("/allocations")
def get_allocations():
    return allocations