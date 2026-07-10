from sqlalchemy.orm import Session

from app.models.co_po_mapping import COPOMapping
from app.schemas.co_po_mapping import (
    COPOMappingCreate,
    COPOMappingUpdate
)


class COPOMappingService:

    @staticmethod
    def create_mapping(db: Session, data: COPOMappingCreate):

        mapping = db.query(COPOMapping).filter(
            COPOMapping.course_outcome_id == data.course_outcome_id,
            COPOMapping.program_outcome_id == data.program_outcome_id
        ).first()

        if mapping:
            raise Exception("CO-PO Mapping already exists")

        if data.mapping_level not in [1, 2, 3]:
            raise Exception("Mapping level must be 1, 2 or 3")

        new_mapping = COPOMapping(
            course_outcome_id=data.course_outcome_id,
            program_outcome_id=data.program_outcome_id,
            mapping_level=data.mapping_level
        )

        db.add(new_mapping)
        db.commit()
        db.refresh(new_mapping)

        return new_mapping

    @staticmethod
    def get_mappings(db: Session):
        return db.query(COPOMapping).all()

    @staticmethod
    def get_mapping(db: Session, mapping_id: int):

        mapping = db.query(COPOMapping).filter(
            COPOMapping.id == mapping_id
        ).first()

        if not mapping:
            raise Exception("CO-PO Mapping not found")

        return mapping

    @staticmethod
    def update_mapping(db: Session, mapping_id: int, data: COPOMappingUpdate):

        mapping = db.query(COPOMapping).filter(
            COPOMapping.id == mapping_id
        ).first()

        if not mapping:
            raise Exception("CO-PO Mapping not found")

        update_data = data.model_dump(exclude_unset=True)

        if "mapping_level" in update_data:
            if update_data["mapping_level"] not in [1, 2, 3]:
                raise Exception("Mapping level must be 1, 2 or 3")

        for key, value in update_data.items():
            setattr(mapping, key, value)

        db.commit()
        db.refresh(mapping)

        return mapping

    @staticmethod
    def delete_mapping(db: Session, mapping_id: int):

        mapping = db.query(COPOMapping).filter(
            COPOMapping.id == mapping_id
        ).first()

        if not mapping:
            raise Exception("CO-PO Mapping not found")

        db.delete(mapping)
        db.commit()

        return {"message": "CO-PO Mapping deleted successfully"}