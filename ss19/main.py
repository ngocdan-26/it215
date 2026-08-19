from fastapi import FastAPI
from ss19.routers.waybill import router_waybill
from ss19.routers.package import router_packge
from ss19.routers.warehouse import router_warehouse


app= FastAPI()

app.include_router(router_waybill)
app.include_router(router_packge)
app.include_router(router_warehouse)