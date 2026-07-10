from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.program import (
    ProgramCreate,
    ProgramUpdate,
    ProgramResponse
)
from app.services.program_service import ProgramService
from app.dependencies.auth import role_required

router = APIRouter(
    prefix="/programs",
    tags=["Program"]
)


@router.post("/", response_model=ProgramResponse)
def create_program(
    data: ProgramCreate,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return ProgramService.create_program(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[ProgramResponse])
def get_programs(
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    return ProgramService.get_programs(db)


@router.get("/{program_id}", response_model=ProgramResponse)
def get_program(
    program_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    try:
        return ProgramService.get_program(db, program_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{program_id}", response_model=ProgramResponse)
def update_program(
    program_id: int,
    data: ProgramUpdate,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return ProgramService.update_program(
            db,
            program_id,
            data
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{program_id}")
def delete_program(
    program_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return ProgramService.delete_program(db, program_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))