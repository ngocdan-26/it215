from pydantic import BaseModel
from ss19.schema.package import PackageResponse
class WarehouseCreate(BaseModel):
    warehouse_name: str
    location: str

class WarehouseDetailResponse(BaseModel):
    id: int
    warehouse_name: str
    location: str
    packages: list[PackageResponse]

    model_config = {
        "from_attributes": True
    }