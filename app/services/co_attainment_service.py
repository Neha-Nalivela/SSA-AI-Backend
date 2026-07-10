from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.student_mark import StudentMark
from app.models.question_co_mapping import QuestionCOMap


class COAttainmentService:

    @staticmethod
    def calculate_co_attainment(
        db: Session,
        course_outcome_id: int
    ):
        """
        Calculate attainment percentage for a Course Outcome (CO).
        """

        mappings = db.query(QuestionCOMap).filter(
            QuestionCOMap.course_outcome_id == course_outcome_id
        ).all()

        if not mappings:
            raise Exception("No Question-CO mappings found")

        question_ids = [m.question_id for m in mappings]

        marks = db.query(StudentMark).filter(
            StudentMark.question_id.in_(question_ids)
        ).all()

        if not marks:
            raise Exception("No student marks found")

        total_obtained = sum(mark.marks_obtained for mark in marks)
        total_max = sum(mark.max_marks for mark in marks)

        if total_max == 0:
            attainment = 0.0
        else:
            attainment = round((total_obtained / total_max) * 100, 2)

        return {
            "course_outcome_id": course_outcome_id,
            "attainment_percentage": attainment
        }