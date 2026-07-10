from pydantic import BaseModel
from typing import Optional


class QuestionCreate(BaseModel):
    question_number: str
    question_text: str
    max_marks: int
    assessment_id: int


class QuestionUpdate(BaseModel):
    question_number: Optional[str] = None
    question_text: Optional[str] = None
    max_marks: Optional[int] = None
    assessment_id: Optional[int] = None
    is_active: Optional[bool] = None


class QuestionResponse(BaseModel):
    id: int
    question_number: str
    question_text: str
    max_marks: int
    assessment_id: int
    is_active: bool

    class Config:
        from_attributes = True