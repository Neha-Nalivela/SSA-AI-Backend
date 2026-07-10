from typing import Optional
from pydantic import BaseModel


class QuestionCOMapCreate(BaseModel):
    question_id: int
    course_outcome_id: int
    weightage: float = 100.0


class QuestionCOMapUpdate(BaseModel):
    question_id: Optional[int] = None
    course_outcome_id: Optional[int] = None
    weightage: Optional[float] = None
    is_active: Optional[bool] = None


class QuestionCOMapResponse(BaseModel):
    id: int
    question_id: int
    course_outcome_id: int
    weightage: float
    is_active: bool

    class Config:
        from_attributes = True