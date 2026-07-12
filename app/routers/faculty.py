from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.faculty import (
    FacultyCreate,
    FacultyUpdate,
    FacultyResponse
)
from app.services.faculty_service import FacultyService
from app.dependencies.auth import role_required

router = APIRouter(
    prefix="/api/faculty",
    tags=["Faculty"]
)


@router.post("/", response_model=FacultyResponse)
def create_faculty(
    data: FacultyCreate,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return FacultyService.create_faculty(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[FacultyResponse])
def get_faculties(
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    return FacultyService.get_faculties(db)


@router.get("/{faculty_id}", response_model=FacultyResponse)
def get_faculty(
    faculty_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    try:
        return FacultyService.get_faculty(db, faculty_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{faculty_id}", response_model=FacultyResponse)
def update_faculty(
    faculty_id: int,
    data: FacultyUpdate,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return FacultyService.update_faculty(db, faculty_id, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{faculty_id}")
def delete_faculty(
    faculty_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return FacultyService.delete_faculty(db, faculty_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))