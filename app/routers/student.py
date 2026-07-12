from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.student import (
    StudentCreate,
    StudentUpdate,
    StudentResponse
)
from app.services.student_service import StudentService
from app.dependencies.auth import role_required

router = APIRouter(
    prefix="/api/students",
    tags=["Student"]
)


@router.post("/", response_model=StudentResponse)
def create_student(
    data: StudentCreate,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return StudentService.create_student(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[StudentResponse])
def get_students(
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    return StudentService.get_students(db)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    try:
        return StudentService.get_student(db, student_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    data: StudentUpdate,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return StudentService.update_student(db, student_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return StudentService.delete_student(db, student_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))