from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ss18.bai3.database.database import get_db
from ss18.bai3.services.student import get_student_courses


router_student = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router_student.get("/{student_id}/courses",)
def student_courses(student_id: int,db: Session = Depends(get_db)):
    return get_student_courses(student_id, db)