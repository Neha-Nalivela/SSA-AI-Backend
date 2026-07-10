from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.course_outcome import (
    CourseOutcomeCreate,
    CourseOutcomeUpdate,
    CourseOutcomeResponse
)
from app.services.course_outcome_service import CourseOutcomeService
from app.dependencies.auth import role_required

router = APIRouter(
    prefix="/course-outcomes",
    tags=["Course Outcome"]
)


@router.post("/", response_model=CourseOutcomeResponse)
def create_course_outcome(
    data: CourseOutcomeCreate,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return CourseOutcomeService.create_course_outcome(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[CourseOutcomeResponse])
def get_course_outcomes(
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    return CourseOutcomeService.get_course_outcomes(db)


@router.get("/{co_id}", response_model=CourseOutcomeResponse)
def get_course_outcome(
    co_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    try:
        return CourseOutcomeService.get_course_outcome(db, co_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{co_id}", response_model=CourseOutcomeResponse)
def update_course_outcome(
    co_id: int,
    data: CourseOutcomeUpdate,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return CourseOutcomeService.update_course_outcome(
            db,
            co_id,
            data
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{co_id}")
def delete_course_outcome(
    co_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return CourseOutcomeService.delete_course_outcome(db, co_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))