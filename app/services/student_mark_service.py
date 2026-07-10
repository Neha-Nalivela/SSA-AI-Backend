from sqlalchemy.orm import Session

from app.models.student_mark import StudentMark
from app.schemas.student_mark import (
    StudentMarkCreate,
    StudentMarkUpdate
)


class StudentMarkService:

    @staticmethod
    def create_mark(db: Session, data: StudentMarkCreate):

        mark = StudentMark(**data.model_dump())

        db.add(mark)
        db.commit()
        db.refresh(mark)

        return mark

    @staticmethod
    def get_marks(db: Session):
        return db.query(StudentMark).all()

    @staticmethod
    def get_mark(db: Session, mark_id: int):
        mark = db.query(StudentMark).filter(
            StudentMark.id == mark_id
        ).first()

        if not mark:
            raise Exception("Student mark not found")

        return mark

    @staticmethod
    def update_mark(db: Session, mark_id: int, data: StudentMarkUpdate):
        mark = db.query(StudentMark).filter(
            StudentMark.id == mark_id
        ).first()

        if not mark:
            raise Exception("Student mark not found")

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(mark, key, value)

        db.commit()
        db.refresh(mark)

        return mark

    @staticmethod
    def delete_mark(db: Session, mark_id: int):
        mark = db.query(StudentMark).filter(
            StudentMark.id == mark_id
        ).first()

        if not mark:
            raise Exception("Student mark not found")

        db.delete(mark)
        db.commit()

        return {"message": "Student mark deleted successfully"}