from model.classroom import Classroom
from model.student import Student
from model.course import Course
from model.enrollment import Enrollment
from model.user import User
from model.user_profile import UserProfile

from fastapi import FastAPI
from router.student import router_student


app = FastAPI()

app.include_router(router_student)


@app.get("/")
def home():
    return {
        "message": "Chạy thành công"
    }