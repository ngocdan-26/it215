from fastapi import FastAPI
from routers.student import router_student

app = FastAPI()

app.include_router(router_student)

@app.get("/")
def test():
    return {
        "message":"test"
    }