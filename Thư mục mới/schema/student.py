from pydantic import BaseModel


class CreatStudent(BaseModel):
    student_code:str
    full_name:str
    email:str
    class_id:int