from fastapi import HTTPException
from sqlalchemy.orm import Session

from ss18.bai3.models.student import Student
from ss18.bai3.models.course import Course
from ss18.bai3.models.enrollment import Enrollment

def get_student_courses(student_id: int, db: Session):
    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Sinh viên không tồn tại"
        )

    courses = (
        db.query(Course)
        .join(
            Enrollment,
            Enrollment.course_id == Course.id
        )
        .filter(
            Enrollment.student_id == student_id
        )
        .all()
    )

    return {
        "student_id": student.id,
        "full_name": student.full_name,
        "courses": courses
    }
