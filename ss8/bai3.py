from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field
from typing import Optional, Literal

app = FastAPI()

desks = [
    {"id": 1, "desk_number": "DSK-A-01", "zone": "Zone A - Quiet Space", "price_per_day": 150000.0, "status": "AVAILABLE"},
    {"id": 2, "desk_number": "DSK-B-02", "zone": "Zone B - Creative", "price_per_day": 200000.0, "status": "AVAILABLE"},
    {"id": 3, "desk_number": "DSK-C-03", "zone": "Zone C - Panoramic", "price_per_day": 250000.0, "status": "MAINTENANCE"}
]

bookings = [
    {
        "id": 1,
        "desk_id": 1,
        "customer_name": "Nguyen Van A",
        "booking_date": "2026-07-01",
        "payment_status": "PAID"
    }
]


class DeskRequest(BaseModel):
    desk_number: str
    zone: str
    price_per_day: float = Field(gt=0)
    status: Literal["AVAILABLE", "UNAVAILABLE", "MAINTENANCE"]


class BookingRequest(BaseModel):
    desk_id: int
    customer_name: str
    booking_date: str
    payment_status: Literal["PENDING", "PAID", "CANCELLED"]


@app.post("/desks", status_code=status.HTTP_201_CREATED)
def create_desk(desk_request: DeskRequest):
    desk_request = desk_request.model_dump()

    for desk in desks:
        if desk["desk_number"] == desk_request["desk_number"]:
            raise HTTPException(
                status_code=400,
                detail="Desk number already exists"
            )

    new_desk = {
        "id": len(desks) + 1,
        **desk_request
    }

    desks.append(new_desk)

    return new_desk


@app.get("/desks")
def get_desks(
    zone_keyword: Optional[str] = None,
    max_price: Optional[float] = None,
    status: Optional[str] = None
):
    result = desks

    if zone_keyword:
        result = [
            desk for desk in result
            if zone_keyword.lower() in desk["zone"].lower()
        ]

    if max_price is not None:
        result = [
            desk for desk in result
            if desk["price_per_day"] <= max_price
        ]

    if status:
        result = [
            desk for desk in result
            if desk["status"] == status
        ]

    return result


@app.get("/desks/{desk_id}")
def get_desk(desk_id: int):
    for desk in desks:
        if desk["id"] == desk_id:
            return desk

    raise HTTPException(
        status_code=404,
        detail="Desk not found"
    )


@app.put("/desks/{desk_id}")
def update_desk(desk_id: int, desk_request: DeskRequest):
    desk_request = desk_request.model_dump()

    for desk in desks:
        if (
            desk["desk_number"] == desk_request["desk_number"]
            and desk["id"] != desk_id
        ):
            raise HTTPException(
                status_code=400,
                detail="Desk number already exists"
            )

    for desk in desks:
        if desk["id"] == desk_id:
            desk.update(desk_request)
            return desk

    raise HTTPException(
        status_code=404,
        detail="Desk not found"
    )


@app.delete("/desks/{desk_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_desk(desk_id: int):
    for desk in desks:
        if desk["id"] == desk_id:
            desks.remove(desk)
            return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=404,
        detail="Desk not found"
    )


@app.post("/bookings", status_code=status.HTTP_201_CREATED)
def create_booking(booking_request: BookingRequest):
    booking_request = booking_request.model_dump()

    desk = None

    for item in desks:
        if item["id"] == booking_request["desk_id"]:
            desk = item
            break

    if desk is None:
        raise HTTPException(
            status_code=404,
            detail="Desk not found"
        )

    if desk["status"] != "AVAILABLE":
        raise HTTPException(
            status_code=400,
            detail="Desk is not available"
        )

    for booking in bookings:
        if (
            booking["desk_id"] == booking_request["desk_id"]
            and booking["booking_date"] == booking_request["booking_date"]
        ):
            raise HTTPException(
                status_code=400,
                detail="Desk already booked on this date"
            )

    new_booking = {
        "id": max([booking["id"] for booking in bookings], default=0) + 1,
        **booking_request
    }

    bookings.append(new_booking)

    return new_booking


@app.get("/bookings")
def get_bookings():
    return bookings