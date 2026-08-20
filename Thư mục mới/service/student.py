
from fastapi import HTTPException

from models.classroom import Classrooms
from models.student import Students


def get_all_student(db):
    student = db.query(Students).all()
    return{
        "statusCode": 200,
        "message": "Lấy danh sách sinh viên thành công!",
        "data": student,
        "error": None,
        "path": "/students"
    }

def add_new_student(student,db):
    classroom = db.query(Classrooms).filter(student.class_id == Classrooms.id).first()
    if classroom is None:
        return{
            "statusCode": 404,
            "message": "Không tìm thấy lớp học!",
            "data": None,
            "error": "ERR-CLASS-01",
            "path": "/students"
        }

    new_student = Students(
        student_code = student.student_code,
        full_name = student.full_name,
        email = student.email,
        class_id = student.class_id
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return{
        "statusCode": 201,
        "message": "Thêm mới sinh viên thành công!",
        "data": new_student,
        "error": None,
        "path": "/students"
    }