from sqlalchemy.orm import Session

from app.models.question import Question
from app.schemas.question import (
    QuestionCreate,
    QuestionUpdate
)


class QuestionService:

    @staticmethod
    def create_question(db: Session, data: QuestionCreate):

        new_question = Question(
            question_number=data.question_number,
            question_text=data.question_text,
            max_marks=data.max_marks,
            assessment_id=data.assessment_id
        )

        db.add(new_question)
        db.commit()
        db.refresh(new_question)

        return new_question

    @staticmethod
    def get_questions(db: Session):
        return db.query(Question).all()

    @staticmethod
    def get_question(db: Session, question_id: int):

        question = db.query(Question).filter(
            Question.id == question_id
        ).first()

        if not question:
            raise Exception("Question not found")

        return question

    @staticmethod
    def update_question(
        db: Session,
        question_id: int,
        data: QuestionUpdate
    ):

        question = db.query(Question).filter(
            Question.id == question_id
        ).first()

        if not question:
            raise Exception("Question not found")

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(question, key, value)

        db.commit()
        db.refresh(question)

        return question

    @staticmethod
    def delete_question(db: Session, question_id: int):

        question = db.query(Question).filter(
            Question.id == question_id
        ).first()

        if not question:
            raise Exception("Question not found")

        db.delete(question)
        db.commit()

        return {"message": "Question deleted successfully"}