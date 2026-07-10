from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.department import (
    DepartmentCreate,
    DepartmentUpdate
)

from app.services.department_service import DepartmentService

from app.dependencies.auth import role_required


router = APIRouter(
    prefix="/departments",
    tags=["Department"]
)


@router.post("/")
def create_department(
    data: DepartmentCreate,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return DepartmentService.create_department(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
def get_departments(
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    return DepartmentService.get_departments(db)


@router.get("/{department_id}")
def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    try:
        return DepartmentService.get_department(db, department_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{department_id}")
def update_department(
    department_id: int,
    data: DepartmentUpdate,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return DepartmentService.update_department(
            db,
            department_id,
            data
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{department_id}")
def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return DepartmentService.delete_department(
            db,
            department_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))