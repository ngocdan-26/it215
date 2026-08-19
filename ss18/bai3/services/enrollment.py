from fastapi import HTTPException

from ss18.bai3.models.student import Student
from ss18.bai3.models.course import Course
from ss18.bai3.models.enrollment import Enrollment


def create_enrollment(data,db):
    student = db.query(Student).filter(Student.id == data.student_id).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Sinh viên không tồn tại"
        )

    course = db.query(Course).filter(Course.id == data.course_id).first()
    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Khóa học không tồn tại"
        )

    if student.status != "ACTIVE":
        raise HTTPException(
            status_code=400,
            detail="Sinh viên không ở trạng thái ACTIVE"
        )

    if course.status != "OPEN":
        raise HTTPException(
            status_code=400,
            detail="Khóa học đã đóng"
        )

    enrollment = db.query(Enrollment).filter(Enrollment.student_id == data.student_id,Enrollment.course_id == data.course_id).first()

    if enrollment is not None:
        raise HTTPException(
            status_code=400,
            detail="Sinh viên đã đăng ký khóa học này"
        )

    current_count = db.query(Enrollment).filter(Enrollment.course_id == data.course_id).count()
    
    if current_count >= course.max_students:
        raise HTTPException(
            status_code=400,
            detail="Khóa học đã đủ số lượng"
        )

    new_enrollment = Enrollment(
        student_id=data.student_id,
        course_id=data.course_id
    )

    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)

    return new_enrollment