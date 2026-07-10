from sqlalchemy.orm import Session

from app.models.faculty import Faculty
from app.schemas.faculty import FacultyCreate, FacultyUpdate


class FacultyService:

    @staticmethod
    def create_faculty(db: Session, data: FacultyCreate):

        faculty = db.query(Faculty).filter(
            Faculty.employee_id == data.employee_id
        ).first()

        if faculty:
            raise Exception("Employee ID already exists")

        faculty = db.query(Faculty).filter(
            Faculty.email == data.email
        ).first()

        if faculty:
            raise Exception("Email already exists")

        new_faculty = Faculty(
            employee_id=data.employee_id,
            name=data.name,
            email=data.email,
            phone=data.phone,
            designation=data.designation,
            qualification=data.qualification,
            specialization=data.specialization,
            department_id=data.department_id
        )

        db.add(new_faculty)
        db.commit()
        db.refresh(new_faculty)

        return new_faculty

    @staticmethod
    def get_faculties(db: Session):
        return db.query(Faculty).all()

    @staticmethod
    def get_faculty(db: Session, faculty_id: int):

        faculty = db.query(Faculty).filter(
            Faculty.id == faculty_id
        ).first()

        if not faculty:
            raise Exception("Faculty not found")

        return faculty

    @staticmethod
    def update_faculty(
        db: Session,
        faculty_id: int,
        data: FacultyUpdate
    ):

        faculty = db.query(Faculty).filter(
            Faculty.id == faculty_id
        ).first()

        if not faculty:
            raise Exception("Faculty not found")

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(faculty, key, value)

        db.commit()
        db.refresh(faculty)

        return faculty

    @staticmethod
    def delete_faculty(db: Session, faculty_id: int):

        faculty = db.query(Faculty).filter(
            Faculty.id == faculty_id
        ).first()

        if not faculty:
            raise Exception("Faculty not found")

        db.delete(faculty)
        db.commit()

        return {"message": "Faculty deleted successfully"}