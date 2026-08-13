from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from schema import SlotCreate
from database import get_db
from services import add_new_slot

router = APIRouter(
    prefix="/boarding-slots",
    tags=["/boarding-slots"]
)

@router.post("")
def add_slot(slot:SlotCreate,db:Session = Depends(get_db)):
    return add_new_slot(slot,db)