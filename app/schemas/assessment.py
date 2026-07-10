from datetime import date
from typing import Optional

from pydantic import BaseModel


class AssessmentCreate(BaseModel):
    assessment_name: str
    assessment_type: str
    max_marks: int
    exam_date: date
    academic_year: str
    semester: int
    subject_id: int


class AssessmentUpdate(BaseModel):
    assessment_name: Optional[str] = None
    assessment_type: Optional[str] = None
    max_marks: Optional[int] = None
    exam_date: Optional[date] = None
    academic_year: Optional[str] = None
    semester: Optional[int] = None
    subject_id: Optional[int] = None
    is_active: Optional[bool] = None


class AssessmentResponse(BaseModel):
    id: int
    assessment_name: str
    assessment_type: str
    max_marks: int
    exam_date: date
    academic_year: str
    semester: int
    subject_id: int
    is_active: bool

    class Config:
        from_attributes = True