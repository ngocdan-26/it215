from pydantic import BaseModel, Field, EmailStr
from typing import Literal


class StudentBase(BaseModel):
    student_code: str = Field(
        ...,
        min_length=3,
        max_length=20
    )

    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    email: EmailStr

    age: int = Field(
        ...,
        ge=16,
        le=60
    )

    gender: Literal["male", "female", "other"]

    class_id: int = Field(
        ...,
        ge=1
    )


class StudentCreate(StudentBase):
    pass


class ClassroomInfo(BaseModel):
    id: int
    class_code: str
    class_name: str
    max_students: int
    status: str

    class Config:
        from_attributes = True


class StudentResponse(BaseModel):
    id: int
    student_code: str
    full_name: str
    email: EmailStr
    age: int
    gender: Literal["male", "female", "other"]
    class_id: int
    classroom: ClassroomInfo | None = None

    class Config:
        from_attributes = True