from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from ss18.bai3.database.database import get_db
from ss18.bai3.schemas.enrollment import EnrollmentCreate
from ss18.bai3.services.enrollment import create_enrollment


router_enrollment = APIRouter(
    prefix="/enrollment",
    tags=["enrollment"]
)

@router_enrollment.post("")
def register_course(data: EnrollmentCreate,db: Session = Depends(get_db)):
    return create_enrollment(data, db)