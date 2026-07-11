from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.co_attainment_service import COAttainmentService
from app.dependencies.auth import role_required

router = APIRouter(
    prefix="/co-attainment",
    tags=["CO Attainment"]
)


@router.get("/{course_outcome_id}")
def calculate_co_attainment(
    course_outcome_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    return COAttainmentService.calculate_co_attainment(
        db,
        course_outcome_id
    )
@router.post("/calculate/{subject_id}")
def calculate(
    subject_id: int,
    semester: str,
    academic_year: str,
    db: Session = Depends(get_db),
):
    return COAttainmentService.calculate_subject_attainment(
    db=db,
    subject_id=subject_id,
    semester=semester,
    academic_year=academic_year,
)