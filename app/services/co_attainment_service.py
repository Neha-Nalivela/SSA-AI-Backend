from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.student_mark import StudentMark
from app.models.question_co_mapping import QuestionCOMap
from app.models.course_outcome import CourseOutcome
from app.models.attainment import Attainment
from app.models.assessment import Assessment
from app.models.question import Question
class COAttainmentService:

    @staticmethod
    def calculate_co_attainment(
        db: Session,
        course_outcome_id: int,
        subject_id: int,
        semester: str,
        academic_year: str
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

        marks = (
            db.query(StudentMark, Question, Assessment)
            .join(
                Question,
                StudentMark.question_id == Question.id
            )
            .join(
                Assessment,
                StudentMark.assessment_id == Assessment.id
            )
            .filter(
                Question.id.in_(question_ids),
                Assessment.subject_id == subject_id,
                Assessment.semester == int(semester),
                Assessment.academic_year == academic_year
            )
            .all()
        )

        if not marks:
            raise Exception("No student marks found")

        total_obtained = sum(
            mark.marks_obtained
            for mark, question, assessment in marks
        )
        total_max = sum(
            question.max_marks
            for mark, question, assessment in marks
        )

        if total_max == 0:
            attainment = 0.0
        else:
            attainment = round((total_obtained / total_max) * 100, 2)

        return {
            "course_outcome_id": course_outcome_id,
            "attainment_percentage": attainment
        }
    @staticmethod
    def calculate_subject_attainment(
        db: Session,
        subject_id: int,
        semester: str,
        academic_year: str,
    ):

        outcomes = (
            db.query(CourseOutcome)
            .filter(CourseOutcome.subject_id == subject_id)
            .all()
        )

        if not outcomes:
            raise Exception("No Course Outcomes found for this subject")

        results = []

        for co in outcomes:

            result = COAttainmentService.calculate_co_attainment(
                db=db,
                course_outcome_id=co.id,
                subject_id=subject_id,
                semester=semester,
                academic_year=academic_year,
            )

            db.query(Attainment).filter(
                Attainment.course_outcome_id == co.id,
                Attainment.semester == semester,
                Attainment.academic_year == academic_year,
            ).delete()

            attainment = Attainment(
                course_outcome_id=co.id,
                attainment_percentage=result["attainment_percentage"],
                semester=semester,
                academic_year=academic_year,
            )

            db.add(attainment)
            results.append(result)

        db.commit()

        return {
            "subject_id": subject_id,
            "semester": semester,
            "academic_year": academic_year,
            "co_attainments": results
        }