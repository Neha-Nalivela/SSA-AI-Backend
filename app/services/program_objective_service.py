from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.program_objective import ProgramObjective
from app.schemas.program_objective import (
    ProgramObjectiveCreate,
    ProgramObjectiveUpdate,
)


class ProgramObjectiveService:

    @staticmethod
    def create_program_objective(db: Session, data: ProgramObjectiveCreate):
        obj = ProgramObjective(**data.model_dump())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def get_program_objectives(db: Session):
        return db.query(ProgramObjective).all()

    @staticmethod
    def get_program_objective(db: Session, obj_id: int):
        obj = db.query(ProgramObjective).filter(
            ProgramObjective.id == obj_id
        ).first()

        if not obj:
            raise HTTPException(404, "Program Objective not found")

        return obj

    @staticmethod
    def update_program_objective(
        db: Session,
        obj_id: int,
        data: ProgramObjectiveUpdate
    ):
        obj = db.query(ProgramObjective).filter(
            ProgramObjective.id == obj_id
        ).first()

        if not obj:
            raise HTTPException(404, "Program Objective not found")

        for key, value in data.model_dump().items():
            setattr(obj, key, value)

        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def delete_program_objective(db: Session, obj_id: int):
        obj = db.query(ProgramObjective).filter(
            ProgramObjective.id == obj_id
        ).first()

        if not obj:
            raise HTTPException(404, "Program Objective not found")

        db.delete(obj)
        db.commit()

        return {"message": "Program Objective deleted successfully"}