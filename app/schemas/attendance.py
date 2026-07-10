from typing import Optional
from pydantic import BaseModel


class AttendanceCreate(BaseModel):
    student_id: int
    subject_id: int
    total_classes: int
    attended_classes: int
    semester: str
    academic_year: str


class AttendanceUpdate(BaseModel):
    student_id: Optional[int] = None
    subject_id: Optional[int] = None
    total_classes: Optional[int] = None
    attended_classes: Optional[int] = None
    semester: Optional[str] = None
    academic_year: Optional[str] = None


class AttendanceResponse(BaseModel):
    id: int
    student_id: int
    subject_id: int
    total_classes: int
    attended_classes: int
    attendance_percentage: float
    semester: str
    academic_year: str

    class Config:
        from_attributes = True