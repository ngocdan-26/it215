from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
app = FastAPI()

tickets_db = [
    {"id": 1, "movie_name": "Doctor Strange 3", "room_code": "IMAX-01", "quantity": 2, "status": "confirmed"},
    {"id": 2, "movie_name": "Avatar 3", "room_code": "PREMIUM-02", "quantity": 1, "status": "confirmed"}
]

class TicketCreate(BaseModel):
    movie_name: str = Field(..., min_length=1)
    room_code: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=1, le=10)

@app.get("/tickets")
def display_tickets():
    return {
        "statusCode": 200,
        "message": "Lấy danh sách vé thành công!",
        "data": tickets_db,
        "error": None,
        "path": "/tickets"
    }

@app.post("/tickets", status_code=status.HTTP_201_CREATED)
def create_ticket(ticket: TicketCreate):
    for item in tickets_db:
        if (
            item["movie_name"].lower() == ticket.movie_name.lower()
            and item["room_code"].lower() == ticket.room_code.lower()
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Lỗi: Vé xem phim tại phòng chiếu này đã được đặt!",
                    "data": None,
                    "error": "ERR-CINE-01: Ticket conflict for movie and room combination.",
                    "path": "/tickets"
                }
            )
        
    new_ticket = {
        "id": max([t["id"] for t in tickets_db], default=0) + 1,
        "movie_name": ticket.movie_name,
        "room_code": ticket.room_code,
        "quantity": ticket.quantity,
        "status": "confirmed"
    }

    tickets_db.append(new_ticket)

    return{
        "statusCode": 201,
        "message": "Đặt vé thành công!",
        "data": new_ticket,
        "error": None,
        "path": "/tickets"
    }

@app.delete("/tickets/{ticket_id}")
def delete_tickets(ticket_id: int):
    for i, ticket in enumerate(tickets_db):
        if ticket["id"] == ticket_id:
            tickets_db.pop(i)
            return{
                "statusCode": 200,
                "message": "Hủy vé thành công!",
                "data": None,
                "error": None,
                "path": "/tickets/1"
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "statusCode": 404,
            "message": "Lỗi: Không tìm thấy mã vé yêu cầu!",
            "data": None,
            "error": "ERR-CINE-02: Ticket ID does not exist.",
            "path": "/tickets/99"
        }
    )

            