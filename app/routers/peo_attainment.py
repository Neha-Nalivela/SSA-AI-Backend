from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.peo_attainment_service import PEOAttainmentService
from app.dependencies.auth import role_required

router = APIRouter(
    prefix="/peo-attainment",
    tags=["PEO Attainment"]
)


@router.post("/calculate/{peo_id}")
def calculate_peo_attainment(
    peo_id: int,
    semester: str,
    academic_year: str,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    return PEOAttainmentService.calculate(
        db=db,
        peo_id=peo_id,
        semester=semester,
        academic_year=academic_year,
    )