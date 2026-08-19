from fastapi import HTTPException
from ss18.bai4.models.student import Student
from ss18.bai4.models.course import Course
from ss18.bai4.models.enrollment import Enrollment


def get_students_by_course(course_id, db):
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    students = (
        db.query(Student)
        .join(
            Enrollment,
            Student.id == Enrollment.student_id
        )
        .filter(
            Enrollment.course_id == course_id,
            Enrollment.status.in_(
                ["STUDYING", "COMPLETED"]
            ),
            Student.status == "ACTIVE"
        )
        .distinct()
        .order_by(Student.full_name.asc())
        .all()
    )

    return {
        "course_id": course.id,
        "course_name": course.name,
        "total_students": len(students),
        "students": [
            {
                "id": student.id,
                "full_name": student.full_name,
                "email": student.email
            }
            for student in students
        ]
    }