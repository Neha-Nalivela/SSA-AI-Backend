from typing import Optional
from pydantic import BaseModel


class ProgramOutcomeCreate(BaseModel):
    po_code: str
    title: str
    description: Optional[str] = None
    program_id: int


class ProgramOutcomeUpdate(BaseModel):
    po_code: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    program_id: Optional[int] = None
    is_active: Optional[bool] = None


class ProgramOutcomeResponse(BaseModel):
    id: int
    po_code: str
    title: str
    description: Optional[str]
    program_id: int
    is_active: bool

    class Config:
        from_attributes = True