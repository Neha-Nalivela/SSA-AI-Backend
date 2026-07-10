from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.attainment_service import AttainmentService
from app.dependencies.auth import role_required

router = APIRouter(
    prefix="/attainment",
    tags=["Attainment"]
)


@router.get("/co/{course_outcome_id}")
def calculate_co_attainment(
    course_outcome_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    return AttainmentService.calculate_co_attainment(
        db,
        course_outcome_id
    )


@router.get("/po/{program_outcome_id}")
def calculate_po_attainment(
    program_outcome_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    return AttainmentService.calculate_po_attainment(
        db,
        program_outcome_id
    )