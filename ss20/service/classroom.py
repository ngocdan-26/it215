from sqlalchemy.orm import Session

from model.classroom import Classroom
from model.student import Student


def validate_classroom(
    db: Session,
    class_id: int,
    student_id: int | None = None
):
    classroom = (
        db.query(Classroom)
        .filter(Classroom.id == class_id)
        .first()
    )

    if not classroom:
        return None, "Lớp học không tồn tại"

    if classroom.status != "active":
        return None, "Lớp học không hoạt động"

    query = db.query(Student).filter(
        Student.class_id == class_id
    )

    if student_id is not None:
        query = query.filter(
            Student.id != student_id
        )

    student_count = query.count()

    if student_count >= classroom.max_students:
        return None, "Lớp học đã đủ số lượng sinh viên"

    return classroom, None