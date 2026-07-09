from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, field_validator
from typing import Optional

app = FastAPI()

courses = [
    {"id": 1, "code": "PY101", "name": "Python Basic", "duration": 30, "fee": 3000000},
    {"id": 2, "code": "API101", "name": "FastAPI Basic", "duration": 24, "fee": 2500000},
    {"id": 3, "code": "JV101", "name": "Java Basic", "duration": 40, "fee": 4000000}
]


class Course(BaseModel):
    code: str
    name: str
    duration: int
    fee: int

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if not value.strip():
            raise ValueError("Name must not be empty")
        return value

    @field_validator("duration")
    @classmethod
    def validate_duration(cls, value):
        if value <= 0:
            raise ValueError("Duration must be greater than 0")
        return value

    @field_validator("fee")
    @classmethod
    def validate_fee(cls, value):
        if value < 0:
            raise ValueError("Fee must be greater than or equal to 0")
        return value


@app.post("/courses")
def create_course(course: Course):
    for item in courses:
        if item["code"].lower() == course.code.lower():
            raise HTTPException(
                status_code=400,
                detail="Course code already exists"
            )

    new_course = {
        "id": max([c["id"] for c in courses], default=0) + 1,
        "code": course.code,
        "name": course.name,
        "duration": course.duration,
        "fee": course.fee
    }

    courses.append(new_course)

    return {
        "message": "Course created successfully",
        "data": new_course
    }


@app.get("/courses")
def get_courses(
    keyword: Optional[str] = Query(None),
    min_fee: Optional[int] = Query(None),
    max_fee: Optional[int] = Query(None)
):
    result = courses

    if keyword:
        keyword = keyword.lower()
        result = [
            course
            for course in result
            if keyword in course["name"].lower()
            or keyword in course["code"].lower()
        ]

    if min_fee is not None:
        result = [
            course
            for course in result
            if course["fee"] >= min_fee
        ]

    if max_fee is not None:
        result = [
            course
            for course in result
            if course["fee"] <= max_fee
        ]

    return {
        "total": len(result),
        "data": result
    }


@app.get("/courses/{course_id}")
def get_course(course_id: int):
    for course in courses:
        if course["id"] == course_id:
            return course

    raise HTTPException(
        status_code=404,
        detail="Course not found"
    )


@app.put("/courses/{course_id}")
def update_course(course_id: int, updated_course: Course):
    course_index = -1

    for index, course in enumerate(courses):
        if course["id"] == course_id:
            course_index = index
            break

    if course_index == -1:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    for course in courses:
        if (
            course["id"] != course_id
            and course["code"].lower() == updated_course.code.lower()
        ):
            raise HTTPException(
                status_code=400,
                detail="Course code already exists"
            )

    courses[course_index] = {
        "id": course_id,
        "code": updated_course.code,
        "name": updated_course.name,
        "duration": updated_course.duration,
        "fee": updated_course.fee
    }

    return {
        "message": "Course updated successfully",
        "data": courses[course_index]
    }


@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    for course in courses:
        if course["id"] == course_id:
            courses.remove(course)

            return {
                "message": "Course deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Course not found"
    )