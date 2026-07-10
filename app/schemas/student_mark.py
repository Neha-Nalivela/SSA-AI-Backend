from typing import Optional
from pydantic import BaseModel


class StudentMarkCreate(BaseModel):
    student_id: int
    assessment_id: int
    question_id: int
    marks_obtained: float


class StudentMarkUpdate(BaseModel):
    student_id: Optional[int] = None
    assessment_id: Optional[int] = None
    question_id: Optional[int] = None
    marks_obtained: Optional[float] = None
    is_active: Optional[bool] = None


class StudentMarkResponse(BaseModel):
    id: int
    student_id: int
    assessment_id: int
    question_id: int
    marks_obtained: float
    is_active: bool

    class Config:
        from_attributes = True