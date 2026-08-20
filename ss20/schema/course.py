from pydantic import BaseModel, Field


class CourseBase(BaseModel):
    course_code: str = Field(...,
        min_length=2,
        max_length=50,
        description="Mã môn học"
    )
    course_name: str = Field(...,
        min_length=2,
        max_length=100,
        description="Tên môn học"
    )
    credits: int = Field(...,
        gt=0,
        le=10,
        description="Số tín chỉ"
    )

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int
    class Config:
        from_attributes = True