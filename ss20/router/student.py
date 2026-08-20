from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from database.database import get_db
from schema.student import StudentCreate
from service.student import (
    get_students,
    get_student_by_id,
    create_student,
    update_student
)


router_student = APIRouter(
    prefix="/students",
    tags=["Students"]
)


def response_data(
    status_code: int,
    message: str,
    data,
    path: str,
    error=None
):
    return {
        "statusCode": status_code,
        "message": message,
        "data": data,
        "error": error,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "path": path
    }


@router_student.get("/")
def get_all_students(
    search: str | None = Query(
        default=None,
        description="Tìm theo mã sinh viên, tên hoặc email"
    ),
    class_id: int | None = Query(
        default=None,
        ge=1,
        description="Lọc theo ID lớp"
    ),
    db: Session = Depends(get_db)
):
    students = get_students(
        db=db,
        search=search,
        class_id=class_id
    )

    return response_data(
        status_code=200,
        message="Lấy danh sách sinh viên thành công",
        data=students,
        error=None,
        path="/students"
    )


@router_student.get("/{student_id}")
def get_student_detail(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = get_student_by_id(
        db=db,
        student_id=student_id
    )

    return response_data(
        status_code=200,
        message="Lấy thông tin sinh viên thành công",
        data=student,
        error=None,
        path=f"/students/{student_id}"
    )

@router_student.post("/", status_code=201)
def add_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    new_student = create_student(
        db=db,
        student=student
    )

    return response_data(
        status_code=201,
        message="Thêm sinh viên thành công",
        data=new_student,
        error=None,
        path="/students"
    )


@router_student.put("/{student_id}")
def edit_student(
    student_id: int,
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    updated_student = update_student(
        db=db,
        student_id=student_id,
        student=student
    )

    return response_data(
        status_code=200,
        message="Cập nhật sinh viên thành công",
        data=updated_student,
        error=None,
        path=f"/students/{student_id}"
    )