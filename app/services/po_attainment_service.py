from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.student_mark import StudentMark
from app.models.question import Question
from app.models.question_co_mapping import QuestionCOMap
from app.models.co_po_mapping import COPOMapping
from app.models.attainment import Attainment
from app.models.program_outcome import ProgramOutcome

class POAttainmentService:

    @staticmethod
    def calculate(
        db: Session,
        program_outcome_id: int,
        semester: str,
        academic_year: str,
    ):
        records = (
            db.query(
                Attainment.attainment_percentage,
                COPOMapping.mapping_level,
            )
            .join(
                COPOMapping,
                Attainment.course_outcome_id ==
                COPOMapping.course_outcome_id,
            )
            .filter(
                COPOMapping.program_outcome_id == program_outcome_id,
                Attainment.semester == semester,
                Attainment.academic_year == academic_year,
            )
            .all()
        )

        if not records:
            raise Exception("No CO Attainments found")

        weighted_sum = 0
        total_weight = 0

        for attainment, mapping_level in records:
            weighted_sum += attainment * mapping_level
            total_weight += mapping_level

        po_attainment = round(weighted_sum / total_weight, 2)

        db.query(Attainment).filter(
            Attainment.program_outcome_id == program_outcome_id,
            Attainment.semester == semester,
            Attainment.academic_year == academic_year,
        ).delete()

        db.add(
            Attainment(
                course_outcome_id=1,      # temporary because this field is NOT NULL
                program_outcome_id=program_outcome_id,
                attainment_percentage=po_attainment,
                semester=semester,
                academic_year=academic_year,
            )
        )

        db.commit()

        return {
            "program_outcome_id": program_outcome_id,
            "attainment_percentage": po_attainment,
            "attainment_level": (
                "High"
                if po_attainment >= 70
                else "Medium"
                if po_attainment >= 50
                else "Low"
            ),
        }