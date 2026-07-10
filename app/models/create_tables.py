from app.database import Base, engine

from app.models.user import User
from app.models.department import Department
from app.models.student import Student
from app.models.faculty import Faculty
from app.models.subject import Subject
from app.models.assessment import Assessment
from app.models.question import Question
from app.models.program import Program
from app.models.program_outcome import ProgramOutcome
from app.models.course_outcome import CourseOutcome
from app.models.question_co_mapping import QuestionCOMap
from app.models.program_educational_objective import ProgramEducationalObjective
from app.models.program_specific_outcome import ProgramSpecificOutcome
from app.models.student_mark import StudentMark
from app.models.attainment import Attainment
from app.models.attendance import Attendance
Base.metadata.create_all(bind=engine)