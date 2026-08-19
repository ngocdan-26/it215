from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ss18.bai4.database.database import get_db
from ss18.bai4.service import get_students_by_course


router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)

@router.get("/{course_id}/students")
def get_course_students(course_id: int,db: Session = Depends(get_db)):
    return get_students_by_course(course_id,db)