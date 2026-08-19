from pydantic import BaseModel


class CreateCategory(BaseModel):
    cat_name : str