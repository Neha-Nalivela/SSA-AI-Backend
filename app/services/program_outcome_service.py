from sqlalchemy.orm import Session

from app.models.program_outcome import ProgramOutcome
from app.schemas.program_outcome import (
    ProgramOutcomeCreate,
    ProgramOutcomeUpdate
)


class ProgramOutcomeService:

    @staticmethod
    def create_program_outcome(
        db: Session,
        data: ProgramOutcomeCreate
    ):

        po = db.query(ProgramOutcome).filter(
            ProgramOutcome.po_code == data.po_code
        ).first()

        if po:
            raise Exception("Program Outcome code already exists")

        new_po = ProgramOutcome(
            po_code=data.po_code,
            title=data.title,
            description=data.description,
            program_id=data.program_id
        )

        db.add(new_po)
        db.commit()
        db.refresh(new_po)

        return new_po

    @staticmethod
    def get_program_outcomes(db: Session):
        return db.query(ProgramOutcome).all()

    @staticmethod
    def get_program_outcome(
        db: Session,
        po_id: int
    ):

        po = db.query(ProgramOutcome).filter(
            ProgramOutcome.id == po_id
        ).first()

        if not po:
            raise Exception("Program Outcome not found")

        return po

    @staticmethod
    def update_program_outcome(
        db: Session,
        po_id: int,
        data: ProgramOutcomeUpdate
    ):

        po = db.query(ProgramOutcome).filter(
            ProgramOutcome.id == po_id
        ).first()

        if not po:
            raise Exception("Program Outcome not found")

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(po, key, value)

        db.commit()
        db.refresh(po)

        return po

    @staticmethod
    def delete_program_outcome(
        db: Session,
        po_id: int
    ):

        po = db.query(ProgramOutcome).filter(
            ProgramOutcome.id == po_id
        ).first()

        if not po:
            raise Exception("Program Outcome not found")

        db.delete(po)
        db.commit()

        return {
            "message": "Program Outcome deleted successfully"
        }