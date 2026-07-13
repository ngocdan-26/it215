from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Literal

app = FastAPI()

carriers = [
    {"id": 1, "code": "GHN", "name": "Giao Hang Nhanh", "max_weight_capacity": 5000, "status": "ACTIVE"},
    {"id": 2, "code": "GHTK", "name": "Giao Hang Tiet Kiem", "max_weight_capacity": 3000, "status": "ACTIVE"},
    {"id": 3, "code": "VTP", "name": "Viettel Post", "max_weight_capacity": 10000, "status": "SUSPENDED"}
]

shipments = [
    {
        "id": 1,
        "carrier_id": 1,
        "order_reference": "ORD-2026-001",
        "total_weight": 4200,
        "dispatch_date": "2026-07-01",
        "shift": "MORNING"
    }
]


class CarrierRequest(BaseModel):
    code: str
    name: str = Field(min_length=3)
    max_weight_capacity: int = Field(gt=0)
    status: Literal["ACTIVE", "INACTIVE", "SUSPENDED"]


class ShipmentRequest(BaseModel):
    carrier_id: int
    order_reference: str
    total_weight: int = Field(gt=0)
    dispatch_date: str
    shift: Literal["MORNING", "AFTERNOON", "NIGHT"]


@app.post("/carriers")
def create_carrier(carrier_request: CarrierRequest):
    carrier_request = carrier_request.model_dump()

    for carrier in carriers:
        if carrier["code"] == carrier_request["code"]:
            raise HTTPException(status_code=400, detail="Carrier code already exists")

    new_carrier = {
        "id": len(carriers) + 1,
        **carrier_request
    }

    carriers.append(new_carrier)

    return {
        "message": "Thêm đối tác thành công",
        "data": new_carrier
    }


@app.get("/carriers")
def get_carriers(
    keyword: Optional[str] = None,
    status: Optional[str] = None,
    min_weight: Optional[int] = None
):
    result = carriers

    if keyword:
        result = [
            carrier for carrier in result
            if keyword.lower() in carrier["name"].lower()
            or keyword.lower() in carrier["code"].lower()
        ]

    if status:
        result = [
            carrier for carrier in result
            if carrier["status"] == status
        ]

    if min_weight:
        result = [
            carrier for carrier in result
            if carrier["max_weight_capacity"] >= min_weight
        ]

    return result


@app.get("/carriers/{carrier_id}")
def get_carrier(carrier_id: int):
    for carrier in carriers:
        if carrier["id"] == carrier_id:
            return carrier

    raise HTTPException(status_code=404, detail="Carrier not found")


@app.put("/carriers/{carrier_id}")
def update_carrier(carrier_id: int, carrier_request: CarrierRequest):
    carrier_request = carrier_request.model_dump()

    for carrier in carriers:
        if carrier["code"] == carrier_request["code"] and carrier["id"] != carrier_id:
            raise HTTPException(status_code=400, detail="Carrier code already exists")

    for carrier in carriers:
        if carrier["id"] == carrier_id:
            carrier.update(carrier_request)

            return {
                "message": "Cập nhật thành công",
                "data": carrier
            }

    raise HTTPException(status_code=404, detail="Carrier not found")


@app.delete("/carriers/{carrier_id}")
def delete_carrier(carrier_id: int):
    for carrier in carriers:
        if carrier["id"] == carrier_id:
            carriers.remove(carrier)
            return {
                "message": "Xóa thành công"
            }

    raise HTTPException(status_code=404, detail="Carrier not found")


@app.post("/shipments")
def create_shipment(shipment_request: ShipmentRequest):
    shipment_request = shipment_request.model_dump()

    carrier = None

    for item in carriers:
        if item["id"] == shipment_request["carrier_id"]:
            carrier = item
            break

    if carrier is None:
        raise HTTPException(status_code=404, detail="Carrier not found")

    if carrier["status"] != "ACTIVE":
        raise HTTPException(status_code=400, detail="Carrier is not active")

    if shipment_request["total_weight"] > carrier["max_weight_capacity"]:
        raise HTTPException(
            status_code=400,
            detail="Shipment weight exceeds carrier capacity"
        )

    for shipment in shipments:
        if (
            shipment["carrier_id"] == shipment_request["carrier_id"]
            and shipment["dispatch_date"] == shipment_request["dispatch_date"]
            and shipment["shift"] == shipment_request["shift"]
        ):
            raise HTTPException(
                status_code=400,
                detail="Carrier already scheduled in this shift"
            )

    new_shipment = {
        "id": len(shipments) + 1,
        **shipment_request
    }

    shipments.append(new_shipment)

    return {
        "message": "Tạo chuyến giao hàng thành công",
        "data": new_shipment
    }


@app.get("/shipments")
def get_shipments():
    return shipments