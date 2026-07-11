from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.student_mark import StudentMark
from app.models.question import Question
from app.models.question_co_mapping import QuestionCOMapping
from app.models.course_outcome import CourseOutcome
from app.models.attainment import Attainment


def calculate_co_attainment(
    db: Session,
    subject_id: int,
    semester: str,
    academic_year: str,
):
    """
    Calculates CO attainment (%) for a subject and stores it
    in the attainments table.
    """

    course_outcomes = (
        db.query(CourseOutcome)
        .filter(CourseOutcome.subject_id == subject_id)
        .all()
    )

    results = []

    for co in course_outcomes:

        mappings = (
            db.query(QuestionCOMapping.question_id)
            .filter(
                QuestionCOMapping.course_outcome_id == co.id
            )
            .all()
        )

        question_ids = [m.question_id for m in mappings]

        if not question_ids:
            continue

        obtained = (
            db.query(func.sum(StudentMark.marks_obtained))
            .filter(StudentMark.question_id.in_(question_ids))
            .scalar()
        ) or 0

        maximum = (
            db.query(func.sum(Question.max_marks))
            .filter(Question.id.in_(question_ids))
            .scalar()
        ) or 0

        if maximum == 0:
            attainment = 0
        else:
            attainment = round((obtained / maximum) * 100, 2)

        record = Attainment(
            course_outcome_id=co.id,
            attainment_percentage=attainment,
            semester=semester,
            academic_year=academic_year,
        )

        db.add(record)

        results.append({
            "co": co.co_code,
            "attainment": attainment
        })

    db.commit()

    return results