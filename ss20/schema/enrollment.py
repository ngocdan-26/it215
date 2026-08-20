from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class EnrollmentBase(BaseModel):
    student_id: int = Field(...,
        gt=0,
        description="ID sinh viên"
    )
    course_id: int = Field(...,
        gt=0,
        description="ID môn học"
    )
    enrollment_date: Optional[date] = Field(None,
        description="Ngày đăng ký học"
    )

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentResponse(EnrollmentBase):
    id: int
    class Config:
        from_attributes = True