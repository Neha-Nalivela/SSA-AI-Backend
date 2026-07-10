from sqlalchemy.orm import Session

from app.models.question_co_mapping import QuestionCOMap
from app.schemas.question_co_mapping import (
    QuestionCOMapCreate,
    QuestionCOMapUpdate
)


class QuestionCOMapService:

    @staticmethod
    def create_mapping(db: Session, data: QuestionCOMapCreate):

        mapping = db.query(QuestionCOMap).filter(
            QuestionCOMap.question_id == data.question_id,
            QuestionCOMap.course_outcome_id == data.course_outcome_id
        ).first()

        if mapping:
            raise Exception("Mapping already exists")

        new_mapping = QuestionCOMap(
            question_id=data.question_id,
            course_outcome_id=data.course_outcome_id,
            weightage=data.weightage
        )

        db.add(new_mapping)
        db.commit()
        db.refresh(new_mapping)

        return new_mapping

    @staticmethod
    def get_mappings(db: Session):
        return db.query(QuestionCOMap).all()

    @staticmethod
    def get_mapping(db: Session, mapping_id: int):
        mapping = db.query(QuestionCOMap).filter(
            QuestionCOMap.id == mapping_id
        ).first()

        if not mapping:
            raise Exception("Mapping not found")

        return mapping

    @staticmethod
    def update_mapping(db: Session, mapping_id: int, data: QuestionCOMapUpdate):
        mapping = db.query(QuestionCOMap).filter(
            QuestionCOMap.id == mapping_id
        ).first()

        if not mapping:
            raise Exception("Mapping not found")

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(mapping, key, value)

        db.commit()
        db.refresh(mapping)

        return mapping

    @staticmethod
    def delete_mapping(db: Session, mapping_id: int):
        mapping = db.query(QuestionCOMap).filter(
            QuestionCOMap.id == mapping_id
        ).first()

        if not mapping:
            raise Exception("Mapping not found")

        db.delete(mapping)
        db.commit()

        return {"message": "Mapping deleted successfully"}