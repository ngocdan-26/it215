from fastapi import APIRouter,Depends
from ss19.database.database import get_db
from ss19.schema.package import PackageUpdate
from sqlalchemy.orm import Session
from ss19.service.package import update_package

router_packge = APIRouter(
    prefix="/Packages",
    tags=["Packages"]
)

@router_packge.put("/{package_id}")
def patch_package(package_id: int,package: PackageUpdate,db: Session = Depends(get_db)):
    return update_package(package_id,package,db)
