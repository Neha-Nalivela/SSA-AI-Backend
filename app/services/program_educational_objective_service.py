from sqlalchemy.orm import Session

from app.models.program_educational_objective import ProgramEducationalObjective
from app.schemas.program_educational_objective import (
    PEOCreate,
    PEOUpdate
)


class PEOService:

    @staticmethod
    def create_peo(db: Session, data: PEOCreate):

        peo = db.query(ProgramEducationalObjective).filter(
            ProgramEducationalObjective.peo_code == data.peo_code
        ).first()

        if peo:
            raise Exception("PEO code already exists")

        new_peo = ProgramEducationalObjective(
            peo_code=data.peo_code,
            title=data.title,
            description=data.description,
            program_id=data.program_id
        )

        db.add(new_peo)
        db.commit()
        db.refresh(new_peo)

        return new_peo

    @staticmethod
    def get_peos(db: Session):
        return db.query(ProgramEducationalObjective).all()

    @staticmethod
    def get_peo(db: Session, peo_id: int):
        peo = db.query(ProgramEducationalObjective).filter(
            ProgramEducationalObjective.id == peo_id
        ).first()

        if not peo:
            raise Exception("PEO not found")

        return peo

    @staticmethod
    def update_peo(db: Session, peo_id: int, data: PEOUpdate):

        peo = db.query(ProgramEducationalObjective).filter(
            ProgramEducationalObjective.id == peo_id
        ).first()

        if not peo:
            raise Exception("PEO not found")

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(peo, key, value)

        db.commit()
        db.refresh(peo)

        return peo

    @staticmethod
    def delete_peo(db: Session, peo_id: int):

        peo = db.query(ProgramEducationalObjective).filter(
            ProgramEducationalObjective.id == peo_id
        ).first()

        if not peo:
            raise Exception("PEO not found")

        db.delete(peo)
        db.commit()

        return {"message": "PEO deleted successfully"}