from sqlalchemy.orm import Session

from app.models.assessment import Assessment
from app.schemas.assessment import (
    AssessmentCreate,
    AssessmentUpdate
)


class AssessmentService:

    @staticmethod
    def create_assessment(db: Session, data: AssessmentCreate):

        new_assessment = Assessment(
            assessment_name=data.assessment_name,
            assessment_type=data.assessment_type,
            max_marks=data.max_marks,
            exam_date=data.exam_date,
            academic_year=data.academic_year,
            semester=data.semester,
            subject_id=data.subject_id
        )

        db.add(new_assessment)
        db.commit()
        db.refresh(new_assessment)

        return new_assessment

    @staticmethod
    def get_assessments(db: Session):
        return db.query(Assessment).all()

    @staticmethod
    def get_assessment(db: Session, assessment_id: int):

        assessment = db.query(Assessment).filter(
            Assessment.id == assessment_id
        ).first()

        if not assessment:
            raise Exception("Assessment not found")

        return assessment

    @staticmethod
    def update_assessment(
        db: Session,
        assessment_id: int,
        data: AssessmentUpdate
    ):

        assessment = db.query(Assessment).filter(
            Assessment.id == assessment_id
        ).first()

        if not assessment:
            raise Exception("Assessment not found")

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(assessment, key, value)

        db.commit()
        db.refresh(assessment)

        return assessment

    @staticmethod
    def delete_assessment(db: Session, assessment_id: int):

        assessment = db.query(Assessment).filter(
            Assessment.id == assessment_id
        ).first()

        if not assessment:
            raise Exception("Assessment not found")

        db.delete(assessment)
        db.commit()

        return {"message": "Assessment deleted successfully"}