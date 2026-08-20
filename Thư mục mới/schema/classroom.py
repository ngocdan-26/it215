from pydantic import BaseModel

class CreateClassroom(BaseModel):
    class_code:str
    class_name:str