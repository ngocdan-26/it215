from fastapi import HTTPException
from ss19.models.package import Package
def update_package(package_id: int,data,db):
    package = db.query(Package).filter(Package.id == package_id).first()
    
    if not package:
        raise HTTPException(
            status_code=404,
            detail="Package not found"
        )
    try:
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(package, key, value)
        db.commit()
        db.refresh(package)
        return package
    except Exception:
        db.rollback()
        raise
