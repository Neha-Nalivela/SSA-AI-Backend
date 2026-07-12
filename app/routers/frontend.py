from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.auth_service import AuthService
from app.models.student import Student
from app.models.department import Department
router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"request": request}
    )


@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        result = AuthService.login(db, email, password)

        response = RedirectResponse(
            url="/dashboard",
            status_code=303
        )

        response.set_cookie(
            key="access_token",
            value=result["access_token"],
            httponly=True
        )

        return response

    except Exception:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "request": request,
                "error": "Invalid email or password"
            }
        )
@router.get("/students")
def students_page(
    request: Request,
    db: Session = Depends(get_db)
):
    students = db.query(Student).all()

    return templates.TemplateResponse(
        request=request,
        name="students.html",
        context={
            "request": request,
            "students": students
        }
    )
@router.get("/students/add")
def add_student_page(
    request: Request,
    db: Session = Depends(get_db)
):
    departments = db.query(Department).all()

    return templates.TemplateResponse(
        request=request,
        name="add_student.html",
        context={
            "request": request,
            "departments": departments
        }
    )
@router.post("/students/add")
def add_student(
    roll_number: str = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    gender: str = Form(...),
    year: int = Form(...),
    semester: int = Form(...),
    cgpa: float = Form(0),
    attendance: float = Form(0),
    department_id: int = Form(...),
    db: Session = Depends(get_db)
):

    student = Student(
        roll_number=roll_number,
        name=name,
        email=email,
        phone=phone,
        gender=gender,
        year=year,
        semester=semester,
        cgpa=cgpa,
        attendance=attendance,
        department_id=department_id
    )

    db.add(student)
    db.commit()

    return RedirectResponse(
        url="/students",
        status_code=303
    )
@router.get("/students/edit/{id}")
def edit_student_page(
    id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == id).first()
    departments = db.query(Department).all()

    return templates.TemplateResponse(
        request=request,
        name="edit_student.html",
        context={
            "request": request,
            "student": student,
            "departments": departments
        }
    )
@router.get("/students/delete/{id}")
def delete_student(
    id: int,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == id).first()

    if student:
        db.delete(student)
        db.commit()

    return RedirectResponse(
        "/students",
        status_code=303
    )
