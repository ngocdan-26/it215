from pydantic import BaseModel
from typing import Optional

class PackageResponse(BaseModel):
    id: int
    package_code: str
    weight: float

class PackageUpdate(BaseModel):
    package_code: Optional[str] = None
    weight: Optional[float] = None
    warehouse_id: Optional[int] = None
