from fastapi import FastAPI

from ss16.bai3.database.base import Base
from ss16.bai3.database.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Course Management API")

@app.post("/enrollments",status_code=201)
def create_enrollment():
    pass

@app.get("/students/{student_id}/courses")
def get_student_courses(student_id: int):
    pass