from sqlalchemy.orm import Session

from app.models.course_outcome import CourseOutcome
from app.schemas.course_outcome import (
    CourseOutcomeCreate,
    CourseOutcomeUpdate
)


class CourseOutcomeService:

    @staticmethod
    def create_course_outcome(db: Session, data: CourseOutcomeCreate):

        co = db.query(CourseOutcome).filter(
            CourseOutcome.co_code == data.co_code,
            CourseOutcome.subject_id == data.subject_id
        ).first()

        if co:
            raise Exception("Course Outcome already exists")

        new_co = CourseOutcome(
            co_code=data.co_code,
            title=data.title,
            description=data.description,
            subject_id=data.subject_id
        )

        db.add(new_co)
        db.commit()
        db.refresh(new_co)

        return new_co

    @staticmethod
    def get_course_outcomes(db: Session):
        return db.query(CourseOutcome).all()

    @staticmethod
    def get_course_outcome(db: Session, co_id: int):

        co = db.query(CourseOutcome).filter(
            CourseOutcome.id == co_id
        ).first()

        if not co:
            raise Exception("Course Outcome not found")

        return co

    @staticmethod
    def update_course_outcome(
        db: Session,
        co_id: int,
        data: CourseOutcomeUpdate
    ):

        co = db.query(CourseOutcome).filter(
            CourseOutcome.id == co_id
        ).first()

        if not co:
            raise Exception("Course Outcome not found")

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(co, key, value)

        db.commit()
        db.refresh(co)

        return co

    @staticmethod
    def delete_course_outcome(db: Session, co_id: int):

        co = db.query(CourseOutcome).filter(
            CourseOutcome.id == co_id
        ).first()

        if not co:
            raise Exception("Course Outcome not found")

        db.delete(co)
        db.commit()

        return {"message": "Course Outcome deleted successfully"}