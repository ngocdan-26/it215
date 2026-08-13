from pydantic import BaseModel


class studentCreat(BaseModel):
    full_name : str
    email : str
    major : str
    gpa : float