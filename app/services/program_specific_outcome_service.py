from sqlalchemy.orm import Session

from app.models.program_specific_outcome import ProgramSpecificOutcome
from app.schemas.program_specific_outcome import (
    PSOCreate,
    PSOUpdate
)


class PSOService:

    @staticmethod
    def create_pso(db: Session, data: PSOCreate):

        pso = db.query(ProgramSpecificOutcome).filter(
            ProgramSpecificOutcome.pso_code == data.pso_code
        ).first()

        if pso:
            raise Exception("PSO code already exists")

        new_pso = ProgramSpecificOutcome(
            pso_code=data.pso_code,
            title=data.title,
            description=data.description,
            program_id=data.program_id
        )

        db.add(new_pso)
        db.commit()
        db.refresh(new_pso)

        return new_pso

    @staticmethod
    def get_psos(db: Session):
        return db.query(ProgramSpecificOutcome).all()

    @staticmethod
    def get_pso(db: Session, pso_id: int):
        pso = db.query(ProgramSpecificOutcome).filter(
            ProgramSpecificOutcome.id == pso_id
        ).first()

        if not pso:
            raise Exception("PSO not found")

        return pso

    @staticmethod
    def update_pso(db: Session, pso_id: int, data: PSOUpdate):
        pso = db.query(ProgramSpecificOutcome).filter(
            ProgramSpecificOutcome.id == pso_id
        ).first()

        if not pso:
            raise Exception("PSO not found")

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(pso, key, value)

        db.commit()
        db.refresh(pso)

        return pso

    @staticmethod
    def delete_pso(db: Session, pso_id: int):
        pso = db.query(ProgramSpecificOutcome).filter(
            ProgramSpecificOutcome.id == pso_id
        ).first()

        if not pso:
            raise Exception("PSO not found")

        db.delete(pso)
        db.commit()

        return {"message": "PSO deleted successfully"}