from fastapi import FastAPI
from ss18.bai4.router import router

app = FastAPI()
app.include_router(router)