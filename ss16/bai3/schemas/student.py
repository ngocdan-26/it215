from ss16.bai3.schemas.course import CourseResponse
from pydantic import BaseModel

class StudentCoursesResponse(BaseModel):
    student_id: int
    full_name: str
    courses: list[CourseResponse]

    model_config = {
        "from_attributes": True
    }