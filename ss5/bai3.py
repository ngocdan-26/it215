from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

students = [
    {"id": 1, "name": "Nguyen Van A"},
    {"id": 2, "name": "Tran Thi B"},
    {"id": 3, "name": "Le Van C"}
]

courses = [
    {"id": 1, "name": "FastAPI Basic", "capacity": 2},
    {"id": 2, "name": "Python OOP", "capacity": 2}
]

registrations = [
    {"id": 1, "student_id": 1, "course_id": 1},
    {"id": 2, "student_id": 2, "course_id": 1}
]

class RegistrationCreate(BaseModel):
    student_id: int
    course_id: int

@app.post("/registrations", status_code=status.HTTP_201_CREATED)
def create_registration(registration: RegistrationCreate):
    student = None
    for s in students:
        if s["id"] == registration.student_id:
            student = s
            break

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    course = None
    for c in courses:
        if c["id"] == registration.course_id:
            course = c
            break

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    for r in registrations:
        if (
            r["student_id"] == registration.student_id
            and r["course_id"] == registration.course_id
        ):
            raise HTTPException(
                status_code=400,
                detail="Student already registered this course"
            )

    total_registered = 0
    for r in registrations:
        if r["course_id"] == registration.course_id:
            total_registered += 1

    if total_registered >= course["capacity"]:
        raise HTTPException(
            status_code=400,
            detail="Course is full"
        )

    new_registration = {
        "id": len(registrations) + 1,
        "student_id": registration.student_id,
        "course_id": registration.course_id
    }

    registrations.append(new_registration)

    return {
        "message": "Registration created successfully",
        "data": new_registration
    }