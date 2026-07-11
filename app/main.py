from fastapi import FastAPI
import app.routers.auth as auth
import app.routers.department as department
import app.routers.student as student
import app.routers.faculty as faculty
import app.routers.subject as subject
import app.routers.assessment as assessment
import app.routers.question as question
import app.routers.program_outcome as program_outcome
import app.routers.program as program
import app.routers.course_outcome as course_outcome
import app.routers.question_co_mapping as question_co_mapping
import app.routers.program_educational_objective as program_educational_objective
import app.routers.program_specific_outcome as program_specific_outcome 
import app.routers.student_mark as student_mark
import app.routers.attainment as attainment
import app.routers.co_attainment as co_attainment
import app.routers.po_attainment as po_attainment
import app.routers.attendance as attendance
import app.routers.program_objective as program_objective
import app.routers.course_objective as course_objective
import app.routers.feedback as feedback
app = FastAPI(
    title="SSA-AI",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(department.router)
app.include_router(student.router)
app.include_router(faculty.router)
app.include_router(subject.router)
app.include_router(assessment.router)
app.include_router(question.router)
app.include_router(program_outcome.router)
app.include_router(program.router)
app.include_router(course_outcome.router)
app.include_router(question_co_mapping.router)
app.include_router(program_educational_objective.router)
app.include_router(program_specific_outcome.router)
app.include_router(student_mark.router)
app.include_router(attainment.router)
app.include_router(co_attainment.router)
app.include_router(po_attainment.router)
app.include_router(attendance.router)
app.include_router(program_objective.router)
app.include_router(course_objective.router)
app.include_router(feedback.router)

@app.get("/")
def root():
    return {
        "message": "SSA-AI Backend Running Successfully"
    }