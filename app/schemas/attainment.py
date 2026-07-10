from pydantic import BaseModel
from typing import Optional


class AttainmentCreate(BaseModel):
    course_outcome_id: int
    program_outcome_id: Optional[int] = None
    attainment_percentage: float
    semester: str
    academic_year: str


class AttainmentUpdate(BaseModel):
    course_outcome_id: Optional[int] = None
    program_outcome_id: Optional[int] = None
    attainment_percentage: Optional[float] = None
    semester: Optional[str] = None
    academic_year: Optional[str] = None


class AttainmentResponse(BaseModel):
    id: int
    course_outcome_id: int
    program_outcome_id: Optional[int]
    attainment_percentage: float
    semester: str
    academic_year: str

    class Config:
        from_attributes = True