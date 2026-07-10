from sqlalchemy.orm import Session

from app.models.subject import Subject
from app.schemas.subject import SubjectCreate, SubjectUpdate


class SubjectService:

    @staticmethod
    def create_subject(db: Session, data: SubjectCreate):

        subject = db.query(Subject).filter(
            Subject.subject_code == data.subject_code
        ).first()

        if subject:
            raise Exception("Subject code already exists")

        new_subject = Subject(
            subject_code=data.subject_code,
            subject_name=data.subject_name,
            credits=data.credits,
            year=data.year,
            semester=data.semester,
            department_id=data.department_id,
            faculty_id=data.faculty_id
        )

        db.add(new_subject)
        db.commit()
        db.refresh(new_subject)

        return new_subject

    @staticmethod
    def get_subjects(db: Session):
        return db.query(Subject).all()

    @staticmethod
    def get_subject(db: Session, subject_id: int):

        subject = db.query(Subject).filter(
            Subject.id == subject_id
        ).first()

        if not subject:
            raise Exception("Subject not found")

        return subject

    @staticmethod
    def update_subject(
        db: Session,
        subject_id: int,
        data: SubjectUpdate
    ):

        subject = db.query(Subject).filter(
            Subject.id == subject_id
        ).first()

        if not subject:
            raise Exception("Subject not found")

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(subject, key, value)

        db.commit()
        db.refresh(subject)

        return subject

    @staticmethod
    def delete_subject(db: Session, subject_id: int):

        subject = db.query(Subject).filter(
            Subject.id == subject_id
        ).first()

        if not subject:
            raise Exception("Subject not found")

        db.delete(subject)
        db.commit()

        return {"message": "Subject deleted successfully"}