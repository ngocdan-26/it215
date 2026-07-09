from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

app = FastAPI()

students = [
    {"id": 1, "code": "SV001", "name": "Nguyen Van A", "email": "a@gmail.com", "age": 20},
    {"id": 2, "code": "SV002", "name": "Tran Thi B", "email": "b@gmail.com", "age": 22},
    {"id": 3, "code": "SV003", "name": "Le Van C", "email": "c@gmail.com", "age": 18}
]


class Student(BaseModel):
    code: str
    name: str
    email: EmailStr
    age: int

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if not value.strip():
            raise ValueError("Name must not be empty")
        return value

    @field_validator("code")
    @classmethod
    def validate_code(cls, value):
        if not value.strip():
            raise ValueError("Code must not be empty")
        return value

    @field_validator("age")
    @classmethod
    def validate_age(cls, value):
        if value <= 0:
            raise ValueError("Age must be greater than 0")
        return value


@app.post("/students")
def create_student(student: Student):
    for item in students:
        if item["code"].lower() == student.code.lower():
            raise HTTPException(
                status_code=400,
                detail="Student code already exists"
            )

    new_student = {
        "id": max([student["id"] for student in students], default=0) + 1,
        "code": student.code,
        "name": student.name,
        "email": student.email,
        "age": student.age
    }

    students.append(new_student)

    return {
        "message": "Student created successfully",
        "data": new_student
    }


@app.get("/students")
def get_students(
    keyword: Optional[str] = Query(None),
    min_age: Optional[int] = Query(None),
    max_age: Optional[int] = Query(None)
):
    result = students

    if keyword:
        keyword = keyword.lower()

        result = [
            student
            for student in result
            if keyword in student["name"].lower()
            or keyword in student["code"].lower()
            or keyword in student["email"].lower()
        ]

    if min_age is not None:
        result = [
            student
            for student in result
            if student["age"] >= min_age
        ]

    if max_age is not None:
        result = [
            student
            for student in result
            if student["age"] <= max_age
        ]

    return {
        "total": len(result),
        "data": result
    }


@app.get("/students/{student_id}")
def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )


@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):
    student_index = -1

    for index, student in enumerate(students):
        if student["id"] == student_id:
            student_index = index
            break

    if student_index == -1:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    for student in students:
        if (
            student["id"] != student_id
            and student["code"].lower() == updated_student.code.lower()
        ):
            raise HTTPException(
                status_code=400,
                detail="Student code already exists"
            )

    students[student_index] = {
        "id": student_id,
        "code": updated_student.code,
        "name": updated_student.name,
        "email": updated_student.email,
        "age": updated_student.age
    }

    return {
        "message": "Student updated successfully",
        "data": students[student_index]
    }


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            students.remove(student)

            return {
                "message": "Student deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )