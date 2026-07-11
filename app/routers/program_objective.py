from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.program_objective import (
    ProgramObjectiveCreate,
    ProgramObjectiveUpdate,
    ProgramObjectiveResponse,
)
from app.services.program_objective_service import ProgramObjectiveService

router = APIRouter(
    prefix="/program-objectives",
    tags=["Program Objectives"]
)


@router.post("/", response_model=ProgramObjectiveResponse)
def create_program_objective(
    data: ProgramObjectiveCreate,
    db: Session = Depends(get_db)
):
    return ProgramObjectiveService.create_program_objective(db, data)


@router.get("/", response_model=list[ProgramObjectiveResponse])
def get_program_objectives(db: Session = Depends(get_db)):
    return ProgramObjectiveService.get_program_objectives(db)


@router.get("/{obj_id}", response_model=ProgramObjectiveResponse)
def get_program_objective(
    obj_id: int,
    db: Session = Depends(get_db)
):
    return ProgramObjectiveService.get_program_objective(db, obj_id)


@router.put("/{obj_id}", response_model=ProgramObjectiveResponse)
def update_program_objective(
    obj_id: int,
    data: ProgramObjectiveUpdate,
    db: Session = Depends(get_db)
):
    return ProgramObjectiveService.update_program_objective(
        db,
        obj_id,
        data,
    )


@router.delete("/{obj_id}")
def delete_program_objective(
    obj_id: int,
    db: Session = Depends(get_db)
):
    return ProgramObjectiveService.delete_program_objective(db, obj_id)