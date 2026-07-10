from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.program_specific_outcome import (
    PSOCreate,
    PSOUpdate,
    PSOResponse
)
from app.services.program_specific_outcome_service import PSOService
from app.dependencies.auth import role_required

router = APIRouter(
    prefix="/psos",
    tags=["Program Specific Outcomes"]
)


@router.post("/", response_model=PSOResponse)
def create_pso(
    data: PSOCreate,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return PSOService.create_pso(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[PSOResponse])
def get_psos(
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    return PSOService.get_psos(db)


@router.get("/{pso_id}", response_model=PSOResponse)
def get_pso(
    pso_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    try:
        return PSOService.get_pso(db, pso_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{pso_id}", response_model=PSOResponse)
def update_pso(
    pso_id: int,
    data: PSOUpdate,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return PSOService.update_pso(db, pso_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{pso_id}")
def delete_pso(
    pso_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return PSOService.delete_pso(db, pso_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))