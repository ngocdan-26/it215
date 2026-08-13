from fastapi import FastAPI

from ss13.test.router import router

app =FastAPI()
app.include_router(router)

