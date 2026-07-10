from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.program_outcome import (
    ProgramOutcomeCreate,
    ProgramOutcomeUpdate,
    ProgramOutcomeResponse
)
from app.services.program_outcome_service import ProgramOutcomeService
from app.dependencies.auth import role_required

router = APIRouter(
    prefix="/program-outcomes",
    tags=["Program Outcome"]
)


@router.post("/", response_model=ProgramOutcomeResponse)
def create_program_outcome(
    data: ProgramOutcomeCreate,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return ProgramOutcomeService.create_program_outcome(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[ProgramOutcomeResponse])
def get_program_outcomes(
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    return ProgramOutcomeService.get_program_outcomes(db)


@router.get("/{po_id}", response_model=ProgramOutcomeResponse)
def get_program_outcome(
    po_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    try:
        return ProgramOutcomeService.get_program_outcome(db, po_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{po_id}", response_model=ProgramOutcomeResponse)
def update_program_outcome(
    po_id: int,
    data: ProgramOutcomeUpdate,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return ProgramOutcomeService.update_program_outcome(
            db,
            po_id,
            data
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{po_id}")
def delete_program_outcome(
    po_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return ProgramOutcomeService.delete_program_outcome(db, po_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))