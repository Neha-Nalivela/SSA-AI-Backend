from pydantic import BaseModel, EmailStr


class StudentCreate(BaseModel):
    roll_number: str
    name: str
    email: EmailStr
    phone: str | None = None
    gender: str | None = None
    year: int
    semester: int
    cgpa: float = 0.0
    attendance: float = 0.0
    department_id: int


class StudentUpdate(BaseModel):
    roll_number: str | None = None
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    gender: str | None = None
    year: int | None = None
    semester: int | None = None
    cgpa: float | None = None
    attendance: float | None = None
    department_id: int | None = None
    is_active: bool | None = None


class StudentResponse(BaseModel):
    id: int
    roll_number: str
    name: str
    email: EmailStr
    phone: str | None
    gender: str | None
    year: int
    semester: int
    cgpa: float
    attendance: float
    department_id: int
    is_active: bool

    class Config:
        from_attributes = True