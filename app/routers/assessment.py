from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.assessment import (
    AssessmentCreate,
    AssessmentUpdate,
    AssessmentResponse
)
from app.services.assessment_service import AssessmentService
from app.dependencies.auth import role_required

router = APIRouter(
    prefix="/assessments",
    tags=["Assessment"]
)


@router.post("/", response_model=AssessmentResponse)
def create_assessment(
    data: AssessmentCreate,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    try:
        return AssessmentService.create_assessment(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[AssessmentResponse])
def get_assessments(
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    return AssessmentService.get_assessments(db)


@router.get("/{assessment_id}", response_model=AssessmentResponse)
def get_assessment(
    assessment_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    try:
        return AssessmentService.get_assessment(db, assessment_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{assessment_id}", response_model=AssessmentResponse)
def update_assessment(
    assessment_id: int,
    data: AssessmentUpdate,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    try:
        return AssessmentService.update_assessment(
            db,
            assessment_id,
            data
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{assessment_id}")
def delete_assessment(
    assessment_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return AssessmentService.delete_assessment(
            db,
            assessment_id
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))