from typing import Optional
from pydantic import BaseModel


class ProgramCreate(BaseModel):
    program_code: str
    program_name: str
    duration: int


class ProgramUpdate(BaseModel):
    program_code: Optional[str] = None
    program_name: Optional[str] = None
    duration: Optional[int] = None
    is_active: Optional[bool] = None


class ProgramResponse(BaseModel):
    id: int
    program_code: str
    program_name: str
    duration: int
    is_active: bool

    class Config:
        from_attributes = True