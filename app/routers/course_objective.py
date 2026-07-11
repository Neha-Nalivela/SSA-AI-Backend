from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.course_objective import (
    CourseObjectiveCreate,
    CourseObjectiveResponse,
)
from app.services.course_objective_service import CourseObjectiveService

router = APIRouter(prefix="/course-objectives", tags=["Course Objectives"])


@router.post("/", response_model=CourseObjectiveResponse)
def create_course_objective(
    data: CourseObjectiveCreate,
    db: Session = Depends(get_db)
):
    return CourseObjectiveService.create(db, data)


@router.get("/", response_model=list[CourseObjectiveResponse])
def get_course_objectives(db: Session = Depends(get_db)):
    return CourseObjectiveService.get_all(db)