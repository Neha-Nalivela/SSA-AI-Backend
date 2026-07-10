from sqlalchemy.orm import Session

from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate


class StudentService:

    @staticmethod
    def create_student(db: Session, data: StudentCreate):

        student = db.query(Student).filter(
            Student.roll_number == data.roll_number
        ).first()

        if student:
            raise Exception("Roll number already exists")

        student = db.query(Student).filter(
            Student.email == data.email
        ).first()

        if student:
            raise Exception("Email already exists")

        new_student = Student(
            roll_number=data.roll_number,
            name=data.name,
            email=data.email,
            phone=data.phone,
            gender=data.gender,
            year=data.year,
            semester=data.semester,
            cgpa=data.cgpa,
            attendance=data.attendance,
            department_id=data.department_id
        )

        db.add(new_student)
        db.commit()
        db.refresh(new_student)

        return new_student

    @staticmethod
    def get_students(db: Session):
        return db.query(Student).all()

    @staticmethod
    def get_student(db: Session, student_id: int):

        student = db.query(Student).filter(
            Student.id == student_id
        ).first()

        if not student:
            raise Exception("Student not found")

        return student

    @staticmethod
    def update_student(db: Session, student_id: int, data: StudentUpdate):

        student = db.query(Student).filter(
            Student.id == student_id
        ).first()

        if not student:
            raise Exception("Student not found")

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(student, key, value)

        db.commit()
        db.refresh(student)

        return student

    @staticmethod
    def delete_student(db: Session, student_id: int):

        student = db.query(Student).filter(
            Student.id == student_id
        ).first()

        if not student:
            raise Exception("Student not found")

        db.delete(student)
        db.commit()

        return {"message": "Student deleted successfully"}