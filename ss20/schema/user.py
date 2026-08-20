from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(...,
        min_length=3,
        max_length=50,
        description="Tên đăng nhập"
    )
    email: str = Field(...,
        min_length=5,
        max_length=100,
        description="Email"
    )

class UserCreate(UserBase):
    password: str = Field(...,
        min_length=6,
        max_length=255,
        description="Mật khẩu"
    )

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True