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
from app.models.mark import Mark

from app.models.faculty import Faculty
from app.models.subject import Subject
from app.models.student_mark import StudentMark
from app.models.attendance import Attendance

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
@router.get("/marks")
def marks_page(
    request: Request,
    db: Session = Depends(get_db)
):
    marks = db.query(Mark).all()

    return templates.TemplateResponse(
        request=request,
        name="marks.html",
        context={
            "request": request,
            "marks": marks
        }
    )


@router.get("/marks/add")
def add_mark_page(
    request: Request,
    assessment_id: int = None,
    db: Session = Depends(get_db)
):
    students = db.query(Student).all()
    assessments = db.query(Assessment).all()

    questions = []

    if assessment_id:
        questions = (
            db.query(Question)
            .filter(Question.assessment_id == assessment_id)
            .all()
        )

    return templates.TemplateResponse(
        "add_mark.html",
        {
            "request": request,
            "students": students,
            "assessments": assessments,
            "questions": questions,
            "selected_assessment": assessment_id
        }
    )


@router.post("/marks/add")
async def add_mark(
    request: Request,
    db: Session = Depends(get_db)
):
    form = await request.form()

    student_id = int(form["student_id"])
    assessment_id = int(form["assessment_id"])

    for key, value in form.items():

        if key.startswith("question_"):

            question_id = int(key.replace("question_", ""))

            mark = Mark(
                student_id=student_id,
                assessment_id=assessment_id,
                question_id=question_id,
                marks_obtained=float(value)
            )

            db.add(mark)

    db.commit()

    return RedirectResponse(
        "/marks",
        status_code=303
    )

@router.get("/marks/edit/{id}")
def edit_mark_page(
    id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    mark = db.query(Mark).filter(Mark.id == id).first()

    students = db.query(Student).all()
    assessments = db.query(Assessment).all()
    questions = db.query(Question).all()

    return templates.TemplateResponse(
        request=request,
        name="edit_mark.html",
        context={
            "request": request,
            "mark": mark,
            "students": students,
            "assessments": assessments,
            "questions": questions
        }
    )


@router.post("/marks/edit/{id}")
def update_mark(
    id: int,
    student_id: int = Form(...),
    assessment_id: int = Form(...),
    question_id: int = Form(...),
    marks_obtained: float = Form(...),
    db: Session = Depends(get_db)
):

    mark = db.query(Mark).filter(Mark.id == id).first()

    mark.student_id = student_id
    mark.assessment_id = assessment_id
    mark.question_id = question_id
    mark.marks_obtained = marks_obtained

    db.commit()

    return RedirectResponse(
        url="/marks",
        status_code=303
    )


@router.get("/marks/delete/{id}")
def delete_mark(
    id: int,
    db: Session = Depends(get_db)
):
    mark = db.query(Mark).filter(Mark.id == id).first()

    if mark:
        db.delete(mark)
        db.commit()

    return RedirectResponse(
        url="/marks",
        status_code=303
    )
@router.get("/questions/by-assessment/{assessment_id}")
def get_questions(
    assessment_id: int,
    db: Session = Depends(get_db)
):
    questions = (
        db.query(Question)
        .filter(Question.assessment_id == assessment_id)
        .all()
    )

    return questions
@router.get("/faculty/dashboard")
def faculty_dashboard(
    request: Request,
    db: Session = Depends(get_db)
):
    total_students = db.query(Student).count()
    total_subjects = db.query(Subject).count()
    total_faculty = db.query(Faculty).count()

    return templates.TemplateResponse(
        request=request,
        name="faculty/dashboard.html",
        context={
            "request": request,
            "total_students": total_students,
            "total_subjects": total_subjects,
            "total_faculty": total_faculty
        }
    )
from app.models.faculty import Faculty


@router.get("/faculty/profile")
def faculty_profile(
    request: Request,
    db: Session = Depends(get_db)
):

    faculty = db.query(Faculty).first()

    return templates.TemplateResponse(
        request=request,
        name="faculty/profile.html",
        context={
            "request": request,
            "faculty": faculty
        }
    )
@router.get("/faculty/subjects")
def faculty_subjects(
    request: Request,
    db: Session = Depends(get_db)
):

    subjects = db.query(Subject).all()

    return templates.TemplateResponse(
        request=request,
        name="faculty/subjects.html",
        context={
            "request": request,
            "subjects": subjects
        }
    )
@router.get("/faculty/subject/{subject_id}")
def faculty_subject_dashboard(
    subject_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    subject = db.query(Subject).filter(
        Subject.id == subject_id
    ).first()

    return templates.TemplateResponse(
        request=request,
        name="faculty/subject_dashboard.html",
        context={
            "request": request,
            "subject": subject
        }
    )
@router.get("/faculty/subject/{subject_id}/students")
def faculty_subject_students(
    subject_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    subject = db.query(Subject).filter(
        Subject.id == subject_id
    ).first()

    # Temporary (until subject-student mapping is implemented)
    students = db.query(Student).all()

    return templates.TemplateResponse(
        request=request,
        name="faculty/students.html",
        context={
            "request": request,
            "subject": subject,
            "students": students
        }
    )
@router.get("/faculty/student/{student_id}")
def faculty_student_profile(
    student_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    return templates.TemplateResponse(
        request=request,
        name="faculty/student_profile.html",
        context={
            "request": request,
            "student": student
        }
    )
from app.models.assessment import Assessment

@router.get("/faculty/subject/{subject_id}/assessments")
def faculty_assessments(
    subject_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    subject = db.query(Subject).filter(
        Subject.id == subject_id
    ).first()

    assessments = db.query(Assessment).filter(
        Assessment.subject_id == subject_id
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="faculty/assessments.html",
        context={
            "request": request,
            "subject": subject,
            "assessments": assessments
        }
    )
@router.get("/faculty/assessment/{assessment_id}")
def faculty_assessment_dashboard(
    assessment_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    assessment = db.query(Assessment).filter(
        Assessment.id == assessment_id
    ).first()

    return templates.TemplateResponse(
        "faculty/assessment_dashboard.html",
        {
            "request": request,
            "assessment": assessment
        }
    )
@router.get("/faculty/assessment/{assessment_id}/marks")
def faculty_marks(
    request: Request,
    assessment_id: int,
    db: Session = Depends(get_db)
):
    assessment = (
        db.query(Assessment)
        .filter(Assessment.id == assessment_id)
        .first()
    )
    students = db.query(Student).all()
    marks = (
        db.query(StudentMark)
        .filter(StudentMark.assessment_id == assessment_id)
        .all()
    )
    mark_dict = {
        m.student_id: m.marks_obtained
        for m in marks
    }
    questions = (
        db.query(Question)
        .filter(Question.assessment_id == assessment_id)
        .all()
    )
    return templates.TemplateResponse(
        request=request,
        name="faculty/marks_entry.html",
        context={
            "request": request,
            "assessment": assessment,
            "students": students,
            "questions": questions,
            "marks": mark_dict
        }
    )
@router.post("/faculty/assessment/{assessment_id}/marks")
async def save_marks(
    request: Request,
    assessment_id: int,
    db: Session = Depends(get_db)
):

    form = await request.form()

    for key, value in form.items():

        if not key.startswith("mark_"):
            continue

        _, student_id, question_id = key.split("_")

        student_id = int(student_id)
        question_id = int(question_id)

        if value == "":
            continue

        mark = db.query(StudentMark).filter(
            StudentMark.student_id == student_id,
            StudentMark.question_id == question_id,
            StudentMark.assessment_id == assessment_id
        ).first()

        if mark:

            mark.marks_obtained = value

        else:

            mark = StudentMark(

                student_id=student_id,

                question_id=question_id,

                assessment_id=assessment_id,

                marks_obtained=value

            )

            db.add(mark)

    db.commit()

    return RedirectResponse(
        url=f"/faculty/assessment/{assessment_id}/marks",
        status_code=303
    )
@router.get("/faculty/subject/{subject_id}/attendance")
def faculty_attendance(
    request: Request,
    subject_id: int,
    db: Session =Depends(get_db)
):

    subject = (
        db.query(Subject)
        .filter(Subject.id == subject_id)
        .first()
    )

    students = db.query(Student).all()

    attendance = (
        db.query(Attendance)
        .filter(Attendance.subject_id == subject_id)
        .all()
    )

    attendance_dict = {
        a.student_id: a
        for a in attendance
    }

    return templates.TemplateResponse(
        request=request,
        name="faculty/attendance.html",
        context={
            "request": request,
            "subject": subject,
            "students": students,
            "attendance": attendance_dict
        }
    )
@router.get("/faculty/assessment/{assessment_id}/questions")
def faculty_questions(
    request: Request,
    assessment_id: int,
    db: Session = Depends(get_db)
):

    assessment = (
        db.query(Assessment)
        .filter(Assessment.id == assessment_id)
        .first()
    )

    questions = (
        db.query(Question)
        .filter(Question.assessment_id == assessment_id)
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="faculty/questions.html",
        context={
            "request": request,
            "assessment": assessment,
            "questions": questions
        }
    )
@router.get("/faculty/assessment/{assessment_id}/question/new")
def new_question(
    request: Request,
    assessment_id: int,
    db: Session = Depends(get_db)
):

    assessment = (
        db.query(Assessment)
        .filter(Assessment.id == assessment_id)
        .first()
    )

    return templates.TemplateResponse(
        request=request,
        name="faculty/add_question.html",
        context={
            "request": request,
            "assessment": assessment
        }
    )
@router.post("/faculty/assessment/{assessment_id}/question/new")
def save_question(
    assessment_id: int,
    question_number: str = Form(...),
    question_text: str = Form(...),
    max_marks: int = Form(...),
    co: str = Form(...),
    btl: str = Form(...),
    db: Session = Depends(get_db)
):

    question = Question(
        assessment_id=assessment_id,
        question_number=question_number,
        question_text=question_text,
        max_marks=max_marks,
        co=co,
        btl=btl
    )

    db.add(question)
    db.commit()

    return RedirectResponse(
        url=f"/faculty/assessment/{assessment_id}/questions",
        status_code=303
    )