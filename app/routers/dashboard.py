from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.student import Student
from app.models.subject import Subject

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):
    total_students = db.query(Student).count()
    total_subjects = db.query(Subject).count()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,          # Required
            "total_students": total_students,
            "total_subjects": total_subjects,
        },
    )