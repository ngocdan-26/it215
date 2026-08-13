from pydantic import BaseModel

class SlotCreate(BaseModel):
    slot_number: str
    room_size: str
    price_per_day: float