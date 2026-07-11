from sqlalchemy.orm import Session
from app.models.course_objective import CourseObjective
from app.schemas.course_objective import CourseObjectiveCreate


class CourseObjectiveService:

    @staticmethod
    def create(db: Session, data: CourseObjectiveCreate):
        obj = CourseObjective(**data.model_dump())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def get_all(db: Session):
        return db.query(CourseObjective).all()