from pydantic import BaseModel


class CreateProduct(BaseModel):
    pro_name:str
    price:float
    cat_id:int