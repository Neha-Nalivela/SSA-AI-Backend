from pydantic import BaseModel
from typing import Optional


class SubjectCreate(BaseModel):
    subject_code: str
    subject_name: str
    credits: int
    year: int
    semester: int
    department_id: int
    faculty_id: int


class SubjectUpdate(BaseModel):
    subject_code: Optional[str] = None
    subject_name: Optional[str] = None
    credits: Optional[int] = None
    year: Optional[int] = None
    semester: Optional[int] = None
    department_id: Optional[int] = None
    faculty_id: Optional[int] = None
    is_active: Optional[bool] = None


class SubjectResponse(BaseModel):
    id: int
    subject_code: str
    subject_name: str
    credits: int
    year: int
    semester: int
    department_id: int
    faculty_id: int
    is_active: bool

    class Config:
        from_attributes = True