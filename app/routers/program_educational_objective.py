from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.program_educational_objective import (
    PEOCreate,
    PEOUpdate,
    PEOResponse
)
from app.services.program_educational_objective_service import PEOService
from app.dependencies.auth import role_required

router = APIRouter(
    prefix="/peos",
    tags=["Program Educational Objectives"]
)


@router.post("/", response_model=PEOResponse)
def create_peo(
    data: PEOCreate,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return PEOService.create_peo(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[PEOResponse])
def get_peos(
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    return PEOService.get_peos(db)


@router.get("/{peo_id}", response_model=PEOResponse)
def get_peo(
    peo_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    try:
        return PEOService.get_peo(db, peo_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{peo_id}", response_model=PEOResponse)
def update_peo(
    peo_id: int,
    data: PEOUpdate,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return PEOService.update_peo(db, peo_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{peo_id}")
def delete_peo(
    peo_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return PEOService.delete_peo(db, peo_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))