from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from schema.student import CreatStudent
from service.student import add_new_student, get_all_student

router_student = APIRouter(
    prefix="/students",
    tags=["students"]
)

@router_student.get("")
def get_student(db:Session=Depends(get_db)):
    return get_all_student(db)

@router_student.post("")
def add_student(student:CreatStudent,db:Session=Depends(get_db)):
    return add_new_student(student,db)
