from pydantic import BaseModel
from typing import Optional


class FeedbackCreate(BaseModel):
    student_id: int
    faculty_id: int
    subject_id: int

    semester: str
    academic_year: str

    teaching_rating: float
    clarity_rating: float
    interaction_rating: float
    practical_rating: float
    assessment_rating: float

    difficult_topic: Optional[str] = None
    suggestions: Optional[str] = None

    completion_time: int


class FeedbackResponse(FeedbackCreate):
    id: int
    reliability_score: float

    class Config:
        from_attributes = True