from fastapi import FastAPI
from ss18.src.routers.category import cat_router
from ss18.src.routers.product import pro_router

app = FastAPI()
app.include_router(cat_router)
app.include_router(pro_router)
@app.get("/")
def test():
    return{
        "message":"api dang chay"
    }