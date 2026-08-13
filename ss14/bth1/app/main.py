from fastapi import FastAPI

from ss14.bth1.app.routers.product import router

app =FastAPI()

app.include_router(router)

