from pydantic import BaseModel
class CourseResponse(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }