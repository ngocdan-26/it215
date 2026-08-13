from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from ss14.bth2.app.database.database import get_db
from ss14.bth2.app.schema.student import studentCreat
from ss14.bth2.app.services.student import add_new_student, delete_student_by_id, get_student,get_student_by_id, update_student_by_id
router = APIRouter(
    prefix="/Students",
    tags=["Students"]
)

@router.get("")
def get_all_student(db:Session=Depends(get_db)):
    return get_student(db)

@router.get("/{stu_id}")
def get_student_detail(stu_id:int,db:Session=Depends(get_db)):
    return get_student_by_id(stu_id,db)

@router.post("")
def add_student(student:studentCreat,db:Session=Depends(get_db)):
    return add_new_student(student,db)

@router.put("/{stu_id}")
def update_student(student:studentCreat,stu_id:int,db:Session=Depends(get_db)):
    return update_student_by_id(student,stu_id,db)

@router.delete("/{stu_id}")
def delete_student(stu_id:int,db:Session=Depends(get_db)):
    return delete_student_by_id(stu_id,db)