from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, field_validator
from typing import Optional

app = FastAPI()

rooms = [
    {"id": 1, "code": "R101", "name": "Room 101", "capacity": 30, "status": "AVAILABLE"},
    {"id": 2, "code": "R102", "name": "Room 102", "capacity": 20, "status": "AVAILABLE"},
    {"id": 3, "code": "R103", "name": "Room 103", "capacity": 40, "status": "MAINTENANCE"}
]

room_bookings = [
    {
        "id": 1,
        "room_id": 1,
        "class_name": "Python Basic",
        "student_count": 25,
        "date": "2026-07-01",
        "slot": "MORNING"
    }
]


class Room(BaseModel):
    code: str
    name: str
    capacity: int
    status: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if not value.strip():
            raise ValueError("Name must not be empty")
        return value

    @field_validator("capacity")
    @classmethod
    def validate_capacity(cls, value):
        if value <= 0:
            raise ValueError("Capacity must be greater than 0")
        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        valid_status = ["AVAILABLE", "IN_USE", "MAINTENANCE"]

        if value not in valid_status:
            raise ValueError(
                "Status must be AVAILABLE, IN_USE or MAINTENANCE"
            )

        return value


class RoomBooking(BaseModel):
    room_id: int
    class_name: str
    student_count: int
    date: str
    slot: str

    @field_validator("class_name")
    @classmethod
    def validate_class_name(cls, value):
        if not value.strip():
            raise ValueError("Class name must not be empty")
        return value

    @field_validator("student_count")
    @classmethod
    def validate_student_count(cls, value):
        if value <= 0:
            raise ValueError("Student count must be greater than 0")
        return value

    @field_validator("slot")
    @classmethod
    def validate_slot(cls, value):
        valid_slots = ["MORNING", "AFTERNOON", "EVENING"]

        if value not in valid_slots:
            raise ValueError(
                "Slot must be MORNING, AFTERNOON or EVENING"
            )

        return value


@app.post("/rooms")
def create_room(room: Room):
    for item in rooms:
        if item["code"].lower() == room.code.lower():
            raise HTTPException(
                status_code=400,
                detail="Room code already exists"
            )

    new_room = {
        "id": max([room["id"] for room in rooms], default=0) + 1,
        "code": room.code,
        "name": room.name,
        "capacity": room.capacity,
        "status": room.status
    }

    rooms.append(new_room)

    return {
        "message": "Room created successfully",
        "data": new_room
    }


@app.get("/rooms")
def get_rooms(
    keyword: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    min_capacity: Optional[int] = Query(None)
):
    result = rooms

    if keyword:
        keyword = keyword.lower()

        result = [
            room
            for room in result
            if keyword in room["code"].lower()
            or keyword in room["name"].lower()
        ]

    if status:
        result = [
            room
            for room in result
            if room["status"] == status
        ]

    if min_capacity is not None:
        result = [
            room
            for room in result
            if room["capacity"] >= min_capacity
        ]

    return {
        "total": len(result),
        "data": result
    }


@app.get("/rooms/{room_id}")
def get_room(room_id: int):
    for room in rooms:
        if room["id"] == room_id:
            return room

    raise HTTPException(
        status_code=404,
        detail="Room not found"
    )


@app.put("/rooms/{room_id}")
def update_room(room_id: int, updated_room: Room):
    room_index = -1

    for index, room in enumerate(rooms):
        if room["id"] == room_id:
            room_index = index
            break

    if room_index == -1:
        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    for room in rooms:
        if (
            room["id"] != room_id
            and room["code"].lower() == updated_room.code.lower()
        ):
            raise HTTPException(
                status_code=400,
                detail="Room code already exists"
            )

    rooms[room_index] = {
        "id": room_id,
        "code": updated_room.code,
        "name": updated_room.name,
        "capacity": updated_room.capacity,
        "status": updated_room.status
    }

    return {
        "message": "Room updated successfully",
        "data": rooms[room_index]
    }


@app.delete("/rooms/{room_id}")
def delete_room(room_id: int):
    for room in rooms:
        if room["id"] == room_id:
            rooms.remove(room)

            return {
                "message": "Room deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Room not found"
    )


@app.post("/room-bookings")
def create_room_booking(booking: RoomBooking):
    room = None

    for item in rooms:
        if item["id"] == booking.room_id:
            room = item
            break

    if room is None:
        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    if room["status"] != "AVAILABLE":
        raise HTTPException(
            status_code=400,
            detail="Room is not available"
        )

    if booking.student_count > room["capacity"]:
        raise HTTPException(
            status_code=400,
            detail="Student count exceeds room capacity"
        )

    for item in room_bookings:
        if (
            item["room_id"] == booking.room_id
            and item["date"] == booking.date
            and item["slot"] == booking.slot
        ):
            raise HTTPException(
                status_code=400,
                detail="Room booking already exists for this date and slot"
            )

    new_booking = {
        "id": max([b["id"] for b in room_bookings], default=0) + 1,
        "room_id": booking.room_id,
        "class_name": booking.class_name,
        "student_count": booking.student_count,
        "date": booking.date,
        "slot": booking.slot
    }

    room_bookings.append(new_booking)

    return {
        "message": "Room booking created successfully",
        "data": new_booking
    }


@app.get("/room-bookings")
def get_room_bookings():
    return {
        "total": len(room_bookings),
        "data": room_bookings
    }