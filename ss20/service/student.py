from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from model.student import Student
from schema.student import StudentCreate
from service.classroom import validate_classroom


def get_students(
    db: Session,
    search: str | None = None,
    class_id: int | None = None
):
    query = (db.query(Student).options(joinedload(Student.classroom)))
    if search:
        keyword = f"%{search}%"
        query = query.filter(
            (Student.student_code.ilike(keyword)) |
            (Student.full_name.ilike(keyword)) |
            (Student.email.ilike(keyword))
        )
    if class_id is not None:
        query = query.filter(
            Student.class_id == class_id
        )
    return query.all()

def get_student_by_id(
    db: Session,
    student_id: int
):
    student = (
        db.query(Student)
        .options(joinedload(Student.classroom))
        .filter(Student.id == student_id)
        .first()
    )
    if not student:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy sinh viên"
        )
    return student


def create_student(
    db: Session,
    student: StudentCreate
):
    existing_code = (
        db.query(Student).filter(Student.student_code == student.student_code).first())

    if existing_code:
        raise HTTPException(
            status_code=400,
            detail="mã sinh viên đã tồn tại"
        )

    existing_email = (
        db.query(Student)
        .filter(
            Student.email == student.email
        )
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="email đã tồn tại"
        )

    classroom, error = validate_classroom(
        db,
        student.class_id
    )

    if error:
        raise HTTPException(
            status_code=400,
            detail=error
        )


    new_student = Student(
        student_code=student.student_code,
        full_name=student.full_name,
        email=str(student.email),
        age=student.age,
        gender=student.gender,
        class_id=student.class_id
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {
        "message": "Thêm thành công",
        "data": new_student
    }


def update_student(
    db: Session,
    student_id: int,
    student: StudentCreate
):

    old_student = (
        db.query(Student)
        .filter(
            Student.id == student_id
        )
        .first()
    )

    if not old_student:
        raise HTTPException(
            status_code=404,
            detail="không tìm thấy sinh viên"
        )

    existing_code = (
        db.query(Student)
        .filter(
            Student.student_code == student.student_code,
            Student.id != student_id
        )
        .first()
    )

    if existing_code:
        raise HTTPException(
            status_code=400,
            detail="mã sinh viên đã tồn tại"
        )

    existing_email = (
        db.query(Student)
        .filter(
            Student.email == student.email,
            Student.id != student_id
        )
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="email đã tồn tại"
        )

    classroom, error = validate_classroom(
        db,
        student.class_id,
        student_id
    )
    if error:
        return None, error

    old_student.student_code = student.student_code
    old_student.full_name = student.full_name
    old_student.email = str(student.email)
    old_student.age = student.age
    old_student.gender = student.gender
    old_student.class_id = student.class_id
    db.commit()
    db.refresh(old_student)
    return {
        "message": "cập nhật thành công",
        "data": old_student
    }