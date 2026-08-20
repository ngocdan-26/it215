from pydantic import BaseModel, Field


class ClassroomBase(BaseModel):
    class_code: str = Field(...,
        min_length=2,
        max_length=50,
        description="Mã lớp"
    )
    class_name: str = Field(...,
        min_length=2,
        max_length=100,
        description="Tên lớp"
    )
    max_students: int = Field(...,
        gt=0,
        description="Số sinh viên tối đa"
    )
    status: str = Field(...,
        max_length=50,
        description="Trạng thái lớp"
    )

class ClassroomCreate(ClassroomBase):
    pass

class ClassroomResponse(ClassroomBase):
    id: int

    class Config:
        from_attributes = True