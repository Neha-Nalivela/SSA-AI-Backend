from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.student_mark import (
    StudentMarkCreate,
    StudentMarkUpdate,
    StudentMarkResponse
)
from app.services.student_mark_service import StudentMarkService
from app.dependencies.auth import role_required

router = APIRouter(
    prefix="/student-marks",
    tags=["Student Marks"]
)


@router.post("/", response_model=StudentMarkResponse)
def create_mark(
    data: StudentMarkCreate,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    try:
        return StudentMarkService.create_mark(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[StudentMarkResponse])
def get_marks(
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    return StudentMarkService.get_marks(db)


@router.get("/{mark_id}", response_model=StudentMarkResponse)
def get_mark(
    mark_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    try:
        return StudentMarkService.get_mark(db, mark_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{mark_id}", response_model=StudentMarkResponse)
def update_mark(
    mark_id: int,
    data: StudentMarkUpdate,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    try:
        return StudentMarkService.update_mark(
            db,
            mark_id,
            data
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{mark_id}")
def delete_mark(
    mark_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return StudentMarkService.delete_mark(db, mark_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))