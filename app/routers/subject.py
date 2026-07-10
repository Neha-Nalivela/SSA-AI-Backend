from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.subject import (
    SubjectCreate,
    SubjectUpdate,
    SubjectResponse
)
from app.services.subject_service import SubjectService
from app.dependencies.auth import role_required

router = APIRouter(
    prefix="/subjects",
    tags=["Subject"]
)


@router.post("/", response_model=SubjectResponse)
def create_subject(
    data: SubjectCreate,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return SubjectService.create_subject(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[SubjectResponse])
def get_subjects(
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    return SubjectService.get_subjects(db)


@router.get("/{subject_id}", response_model=SubjectResponse)
def get_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    try:
        return SubjectService.get_subject(db, subject_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{subject_id}", response_model=SubjectResponse)
def update_subject(
    subject_id: int,
    data: SubjectUpdate,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return SubjectService.update_subject(
            db,
            subject_id,
            data
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{subject_id}")
def delete_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return SubjectService.delete_subject(db, subject_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))