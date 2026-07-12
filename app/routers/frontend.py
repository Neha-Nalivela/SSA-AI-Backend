from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.services.auth_service import AuthService
from app.models.student import Student
from app.models.department import Department
from app.models.subject import Subject
from app.models.faculty import Faculty
from app.models.assessment import Assessment
from app.models.question import Question

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
@router.get("/subjects")
def subjects_page(
    request: Request,
    db: Session = Depends(get_db)
):
    subjects = db.query(Subject).all()

    return templates.TemplateResponse(
        request=request,
        name="subjects.html",
        context={
            "request": request,
            "subjects": subjects
        }
    )
from app.models.department import Department
from app.models.faculty import Faculty

@router.get("/subjects/add")
def add_subject_page(
    request: Request,
    db: Session = Depends(get_db)
):
    departments = db.query(Department).all()
    faculties = db.query(Faculty).all()

    return templates.TemplateResponse(
        request=request,
        name="add_subject.html",
        context={
            "request": request,
            "departments": departments,
            "faculties": faculties
        }
    )
@router.post("/subjects/add")
def add_subject(
    subject_code: str = Form(...),
    subject_name: str = Form(...),
    credits: int = Form(...),
    year: int = Form(...),
    semester: int = Form(...),
    department_id: int = Form(...),
    faculty_id: int = Form(...),
    db: Session = Depends(get_db)
):

    subject = Subject(
        subject_code=subject_code,
        subject_name=subject_name,
        credits=credits,
        year=year,
        semester=semester,
        department_id=department_id,
        faculty_id=faculty_id
    )

    db.add(subject)
    db.commit()

    return RedirectResponse(
        url="/subjects",
        status_code=303
    )
@router.get("/subjects/edit/{id}")
def edit_subject_page(
    id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    subject = db.query(Subject).filter(Subject.id == id).first()

    return templates.TemplateResponse(
        request=request,
        name="edit_subject.html",
        context={
            "request": request,
            "subject": subject
        }
    )
@router.post("/subjects/edit/{id}")
def update_subject(
    id: int,
    subject_code: str = Form(...),
    subject_name: str = Form(...),
    credits: int = Form(...),
    year: int = Form(...),
    semester: int = Form(...),
    department_id: int = Form(...),
    faculty_id: int = Form(...),
    db: Session = Depends(get_db)
):
    subject = db.query(Subject).filter(Subject.id == id).first()

    subject.subject_code = subject_code
    subject.subject_name = subject_name
    subject.credits = credits
    subject.year = year
    subject.semester = semester
    subject.department_id = department_id
    subject.faculty_id = faculty_id

    db.commit()

    return RedirectResponse("/subjects", status_code=303)
@router.get("/subjects/delete/{id}")
def delete_subject(
    id: int,
    db: Session = Depends(get_db)
):
    subject = db.query(Subject).filter(Subject.id == id).first()

    if subject:
        db.delete(subject)
        db.commit()

    return RedirectResponse(
        url="/subjects",
        status_code=303
    )
from app.models.faculty import Faculty

@router.get("/faculty")
def faculty_page(
    request: Request,
    db: Session = Depends(get_db)
):
    faculties = db.query(Faculty).all()

    return templates.TemplateResponse(
        request=request,
        name="faculty.html",
        context={
            "request": request,
            "faculties": faculties
        }
    )
@router.get("/faculty/add")
def add_faculty_page(
    request: Request,
    db: Session = Depends(get_db)
):
    departments = db.query(Department).all()

    return templates.TemplateResponse(
        request=request,
        name="add_faculty.html",
        context={
            "request": request,
            "departments": departments
        }
    )
@router.post("/faculty/add")
def add_faculty(
    employee_id: str = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    designation: str = Form(""),
    qualification: str = Form(""),
    specialization: str = Form(""),
    department_id: int = Form(...),
    db: Session = Depends(get_db)
):

    faculty = Faculty(
        employee_id=employee_id,
        name=name,
        email=email,
        phone=phone,
        designation=designation,
        qualification=qualification,
        specialization=specialization,
        department_id=department_id
    )

    db.add(faculty)
    db.commit()

    return RedirectResponse(
        url="/faculty",
        status_code=303
    )
@router.get("/faculty/edit/{id}")
def edit_faculty_page(
    id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    faculty = db.query(Faculty).filter(Faculty.id == id).first()
    departments = db.query(Department).all()

    return templates.TemplateResponse(
        request=request,
        name="edit_faculty.html",
        context={
            "request": request,
            "faculty": faculty,
            "departments": departments
        }
    )
@router.post("/faculty/edit/{id}")
def update_faculty(
    id: int,
    employee_id: str = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    designation: str = Form(""),
    qualification: str = Form(""),
    specialization: str = Form(""),
    department_id: int = Form(...),
    db: Session = Depends(get_db)
):
    faculty = db.query(Faculty).filter(Faculty.id == id).first()

    faculty.employee_id = employee_id
    faculty.name = name
    faculty.email = email
    faculty.phone = phone
    faculty.designation = designation
    faculty.qualification = qualification
    faculty.specialization = specialization
    faculty.department_id = department_id

    db.commit()

    return RedirectResponse(
        url="/faculty",
        status_code=303
    )
@router.get("/faculty/delete/{id}")
def delete_faculty(
    id: int,
    db: Session = Depends(get_db)
):
    faculty = db.query(Faculty).filter(Faculty.id == id).first()

    if faculty:
        db.delete(faculty)
        db.commit()

    return RedirectResponse(
        url="/faculty",
        status_code=303
    )
@router.get("/assessments")
def assessments_page(
    request: Request,
    db: Session = Depends(get_db)
):
    assessments = db.query(Assessment).all()

    return templates.TemplateResponse(
        request=request,
        name="assessments.html",
        context={
            "request": request,
            "assessments": assessments
        }
    )
@router.get("/assessments/add")
def add_assessment_page(
    request: Request,
    db: Session = Depends(get_db)
):
    subjects = db.query(Subject).all()

    return templates.TemplateResponse(
        request=request,
        name="add_assessment.html",
        context={
            "request": request,
            "subjects": subjects
        }
    )
@router.post("/assessments/add")
def add_assessment(
    assessment_name: str = Form(...),
    assessment_type: str = Form(...),
    max_marks: int = Form(...),
    exam_date: str = Form(...),
    academic_year: str = Form(...),
    semester: int = Form(...),
    subject_id: int = Form(...),
    db: Session = Depends(get_db)
):

    assessment = Assessment(
        assessment_name=assessment_name,
        assessment_type=assessment_type,
        max_marks=max_marks,
        exam_date=exam_date,
        academic_year=academic_year,
        semester=semester,
        subject_id=subject_id
    )

    db.add(assessment)
    db.commit()

    return RedirectResponse(
        url="/assessments",
        status_code=303
    )
@router.get("/assessments/edit/{id}")
def edit_assessment_page(
    id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    assessment = db.query(Assessment).filter(Assessment.id == id).first()
    subjects = db.query(Subject).all()

    return templates.TemplateResponse(
        request=request,
        name="edit_assessment.html",
        context={
            "request": request,
            "assessment": assessment,
            "subjects": subjects
        }
    )
@router.post("/assessments/edit/{id}")
def update_assessment(
    id: int,
    assessment_name: str = Form(...),
    assessment_type: str = Form(...),
    max_marks: int = Form(...),
    exam_date: date = Form(...),
    academic_year: str = Form(...),
    semester: int = Form(...),
    subject_id: int = Form(...),
    db: Session = Depends(get_db)
):
    assessment = db.query(Assessment).filter(Assessment.id == id).first()

    assessment.assessment_name = assessment_name
    assessment.assessment_type = assessment_type
    assessment.max_marks = max_marks
    assessment.exam_date = exam_date
    assessment.academic_year = academic_year
    assessment.semester = semester
    assessment.subject_id = subject_id

    db.commit()

    return RedirectResponse(
        url="/assessments",
        status_code=303
    )
@router.get("/assessments/delete/{id}")
def delete_assessment(
    id: int,
    db: Session = Depends(get_db)
):
    assessment = db.query(Assessment).filter(Assessment.id == id).first()

    if assessment:
        db.delete(assessment)
        db.commit()

    return RedirectResponse(
        url="/assessments",
        status_code=303
    )
@router.get("/questions")
def questions_page(
    request: Request,
    db: Session = Depends(get_db)
):
    questions = db.query(Question).all()

    return templates.TemplateResponse(
        request=request,
        name="questions.html",
        context={
            "request": request,
            "questions": questions
        }
    )
@router.get("/questions/add")
def add_question_page(
    request: Request,
    db: Session = Depends(get_db)
):
    assessments = db.query(Assessment).all()

    return templates.TemplateResponse(
        request=request,
        name="add_question.html",
        context={
            "request": request,
            "assessments": assessments
        }
    )
@router.post("/questions/add")
def add_question(
    question_number: str = Form(...),
    question_text: str = Form(...),
    max_marks: int = Form(...),
    assessment_id: int = Form(...),
    db: Session = Depends(get_db)
):
    question = Question(
        question_number=question_number,
        question_text=question_text,
        max_marks=max_marks,
        assessment_id=assessment_id
    )

    db.add(question)
    db.commit()

    return RedirectResponse(
        url="/questions",
        status_code=303
    )
@router.get("/questions/edit/{id}")
def edit_question_page(
    id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    question = db.query(Question).filter(Question.id == id).first()
    assessments = db.query(Assessment).all()

    return templates.TemplateResponse(
        request=request,
        name="edit_question.html",
        context={
            "request": request,
            "question": question,
            "assessments": assessments
        }
    )
@router.post("/questions/edit/{id}")
def update_question(
    id: int,
    question_number: str = Form(...),
    question_text: str = Form(...),
    max_marks: int = Form(...),
    assessment_id: int = Form(...),
    db: Session = Depends(get_db)
):
    question = db.query(Question).filter(Question.id == id).first()

    question.question_number = question_number
    question.question_text = question_text
    question.max_marks = max_marks
    question.assessment_id = assessment_id

    db.commit()

    return RedirectResponse(
        url="/questions",
        status_code=303
    )
@router.get("/questions/delete/{id}")
def delete_question(
    id: int,
    db: Session = Depends(get_db)
):
    question = db.query(Question).filter(Question.id == id).first()

    if question:
        db.delete(question)
        db.commit()

    return RedirectResponse(
        url="/questions",
        status_code=303
    )
