from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.question_co_mapping import (
    QuestionCOMapCreate,
    QuestionCOMapUpdate,
    QuestionCOMapResponse
)
from app.services.question_co_mapping_service import QuestionCOMapService
from app.dependencies.auth import role_required

router = APIRouter(
    prefix="/question-co-mappings",
    tags=["Question CO Mapping"]
)


@router.post("/", response_model=QuestionCOMapResponse)
def create_mapping(
    data: QuestionCOMapCreate,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return QuestionCOMapService.create_mapping(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[QuestionCOMapResponse])
def get_mappings(
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    return QuestionCOMapService.get_mappings(db)


@router.get("/{mapping_id}", response_model=QuestionCOMapResponse)
def get_mapping(
    mapping_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    try:
        return QuestionCOMapService.get_mapping(db, mapping_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{mapping_id}", response_model=QuestionCOMapResponse)
def update_mapping(
    mapping_id: int,
    data: QuestionCOMapUpdate,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return QuestionCOMapService.update_mapping(
            db,
            mapping_id,
            data
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{mapping_id}")
def delete_mapping(
    mapping_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return QuestionCOMapService.delete_mapping(db, mapping_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))