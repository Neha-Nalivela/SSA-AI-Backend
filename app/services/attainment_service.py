from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.student_mark import StudentMark
from app.models.question import Question
from app.models.question_co_mapping import QuestionCOMap
from app.models.co_po_mapping import COPOMapping


class AttainmentService:

    @staticmethod
    def calculate_co_attainment(db: Session, course_outcome_id: int):

        result = (
            db.query(
                func.avg(
                    (StudentMark.marks_obtained / Question.max_marks) * 100
                )
            )
            .join(
                Question,
                StudentMark.question_id == Question.id
            )
            .join(
                QuestionCOMap,
                Question.id == QuestionCOMap.question_id
            )
            .filter(
                QuestionCOMap.course_outcome_id == course_outcome_id
            )
            .scalar()
        )

        attainment = round(result or 0, 2)

        return {
            "course_outcome_id": course_outcome_id,
            "attainment_percentage": attainment,
            "attainment_level":
                "High" if attainment >= 70 else
                "Medium" if attainment >= 50 else
                "Low"
        }

    @staticmethod
    def calculate_po_attainment(db: Session, program_outcome_id: int):

        result = (
            db.query(
                func.avg(
                    (StudentMark.marks_obtained / Question.max_marks)
                    * 100
                    * COPOMapping.mapping_level
                )
            )
            .join(
                Question,
                StudentMark.question_id == Question.id
            )
            .join(
                QuestionCOMap,
                Question.id == QuestionCOMap.question_id
            )
            .join(
                COPOMapping,
                QuestionCOMap.course_outcome_id ==
                COPOMapping.course_outcome_id
            )
            .filter(
                COPOMapping.program_outcome_id == program_outcome_id
            )
            .scalar()
        )

        attainment = round(result or 0, 2)

        return {
            "program_outcome_id": program_outcome_id,
            "attainment_percentage": attainment,
            "attainment_level":
                "High" if attainment >= 70 else
                "Medium" if attainment >= 50 else
                "Low"
        }