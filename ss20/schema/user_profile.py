from pydantic import BaseModel, Field


class UserProfileBase(BaseModel):
    full_name: str = Field(...,
        min_length=2,
        max_length=100,
        description="Họ và tên"
    )
    phone: str = Field(...,
        min_length=9,
        max_length=20,
        description="Số điện thoại"
    )
    address: str = Field(...,
        min_length=2,
        max_length=255,
        description="Địa chỉ"
    )

class UserProfileCreate(UserProfileBase):
    user_id: int = Field(...,
        gt=0,
        description="ID người dùng"
    )

class UserProfileResponse(UserProfileBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True