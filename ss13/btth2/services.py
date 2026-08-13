from schema import SlotCreate
from models import BoardingSlot


def add_new_slot(slot: SlotCreate,db):
    new_slot = BoardingSlot(
        slot_number = slot.slot_number,
        room_size = slot.room_size,
        price_per_day = slot.price_per_day
    )
    db.add(new_slot)
    db.commit()
    db.refresh(new_slot)
    return{
        "message": "Thêm khoang lưu trú mới thanh cong",
        "data": new_slot
    }   