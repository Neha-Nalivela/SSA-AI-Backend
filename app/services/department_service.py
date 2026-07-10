from sqlalchemy.orm import Session

from app.models.department import Department
from app.schemas.department import (
    DepartmentCreate,
    DepartmentUpdate
)


class DepartmentService:

    @staticmethod
    def create_department(
        db: Session,
        data: DepartmentCreate
    ):

        department = db.query(Department).filter(
            Department.code == data.code
        ).first()

        if department:
            raise Exception("Department already exists")

        department = Department(
            name=data.name,
            code=data.code
        )

        db.add(department)
        db.commit()
        db.refresh(department)

        return department

    @staticmethod
    def get_departments(db: Session):

        return db.query(Department).all()

    @staticmethod
    def get_department(db: Session, department_id: int):

        department = db.query(Department).filter(
            Department.id == department_id
        ).first()

        if not department:
            raise Exception("Department not found")

        return department

    @staticmethod
    def update_department(
        db: Session,
        department_id: int,
        data: DepartmentUpdate
    ):

        department = db.query(Department).filter(
            Department.id == department_id
        ).first()

        if not department:
            raise Exception("Department not found")

        department.name = data.name
        department.code = data.code

        db.commit()
        db.refresh(department)

        return department

    @staticmethod
    def delete_department(
        db: Session,
        department_id: int
    ):

        department = db.query(Department).filter(
            Department.id == department_id
        ).first()

        if not department:
            raise Exception("Department not found")

        db.delete(department)
        db.commit()

        return {"message": "Department deleted successfully"}