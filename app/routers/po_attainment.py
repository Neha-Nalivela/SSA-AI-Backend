from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.po_attainment_service import POAttainmentService
from app.dependencies.auth import role_required

router = APIRouter(
    prefix="/po-attainment",
    tags=["PO Attainment"]
)


@router.get("/{program_outcome_id}")
def calculate_po_attainment(
    program_outcome_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    return POAttainmentService.calculate(
        db,
        program_outcome_id
    )