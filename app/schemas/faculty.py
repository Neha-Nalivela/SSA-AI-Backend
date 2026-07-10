from pydantic import BaseModel, EmailStr
from typing import Optional


class FacultyCreate(BaseModel):
    employee_id: str
    name: str
    email: EmailStr
    phone: Optional[str] = None
    designation: Optional[str] = None
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    department_id: int


class FacultyUpdate(BaseModel):
    employee_id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    designation: Optional[str] = None
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    department_id: Optional[int] = None
    is_active: Optional[bool] = None


class FacultyResponse(BaseModel):
    id: int
    employee_id: str
    name: str
    email: EmailStr
    phone: Optional[str]
    designation: Optional[str]
    qualification: Optional[str]
    specialization: Optional[str]
    department_id: int
    is_active: bool

    class Config:
        from_attributes = True