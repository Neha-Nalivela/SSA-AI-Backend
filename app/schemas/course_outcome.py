from typing import Optional
from pydantic import BaseModel


class CourseOutcomeCreate(BaseModel):
    co_code: str
    title: str
    description: Optional[str] = None
    subject_id: int


class CourseOutcomeUpdate(BaseModel):
    co_code: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    subject_id: Optional[int] = None
    is_active: Optional[bool] = None


class CourseOutcomeResponse(BaseModel):
    id: int
    co_code: str
    title: str
    description: Optional[str]
    subject_id: int
    is_active: bool

    class Config:
        from_attributes = True