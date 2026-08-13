from fastapi import HTTPException

from ss14.bth2.app.models.student import Student


def get_student(db):
    student = db.query(Student).all()
    return{
        "message":"lay danh sach thanh cong",
        "data":student
    }

def get_student_by_id(stu_id:int,db):
    student = db.query(Student).filter(Student.id == stu_id).first()
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="khong tim thay sinh vien"
        )
    return{
        "message":"tim thay sinh vien",
        "data":student
    }

def add_new_student(student,db):
    new_student = Student(
        full_name = student.full_name,
        email = student.email,
        major = student.major,
        gpa = student.gpa
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return{
        "message":"them sinh vien thanh cong",
        "data" : new_student
    }

def update_student_by_id(update_student,stu_id:int,db):
    student = db.query(Student).filter(Student.id == stu_id).first()
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="khong tim thay sinh vien"
        )
    student.full_name = update_student.full_name
    student.email = update_student.email
    student.major = update_student.major
    student.gpa = update_student.gpa
    db.commit()
    db.refresh(student)
    return{
        "message":"cap nhat thong tin sinh vien thanh cong",
        "data":student
    }

def delete_student_by_id(stu_id:int,db):
    student = db.query(Student).filter(Student.id == stu_id).first()
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="khong tim thay sinh vien"
        )
    db.delete(student)
    db.commit()
    return{
        "message":"xoa sinh vien thanh cong",
        "data":student
    }