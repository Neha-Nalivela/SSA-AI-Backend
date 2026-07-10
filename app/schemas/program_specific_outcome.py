from typing import Optional
from pydantic import BaseModel


class PSOCreate(BaseModel):
    pso_code: str
    title: str
    description: Optional[str] = None
    program_id: int


class PSOUpdate(BaseModel):
    pso_code: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    program_id: Optional[int] = None
    is_active: Optional[bool] = None


class PSOResponse(BaseModel):
    id: int
    pso_code: str
    title: str
    description: Optional[str]
    program_id: int
    is_active: bool

    class Config:
        from_attributes = True