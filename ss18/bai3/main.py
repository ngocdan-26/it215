from fastapi import FastAPI
from ss18.bai3.routers.student import router_student
from ss18.bai3.routers.enrollment import router_enrollment

app = FastAPI()
app.include_router(router_enrollment)
app.include_router(router_student)