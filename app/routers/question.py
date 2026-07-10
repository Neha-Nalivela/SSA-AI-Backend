from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.question import (
    QuestionCreate,
    QuestionUpdate,
    QuestionResponse
)
from app.services.question_service import QuestionService
from app.dependencies.auth import role_required

router = APIRouter(
    prefix="/questions",
    tags=["Question"]
)


@router.post("/", response_model=QuestionResponse)
def create_question(
    data: QuestionCreate,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    try:
        return QuestionService.create_question(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[QuestionResponse])
def get_questions(
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    return QuestionService.get_questions(db)


@router.get("/{question_id}", response_model=QuestionResponse)
def get_question(
    question_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    try:
        return QuestionService.get_question(db, question_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{question_id}", response_model=QuestionResponse)
def update_question(
    question_id: int,
    data: QuestionUpdate,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin", "Faculty"))
):
    try:
        return QuestionService.update_question(
            db,
            question_id,
            data
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{question_id}")
def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("Admin"))
):
    try:
        return QuestionService.delete_question(
            db,
            question_id
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))