from fastapi import FastAPI
from ss14.bth2.app.routers.student import router

app = FastAPI()
app.include_router(router)