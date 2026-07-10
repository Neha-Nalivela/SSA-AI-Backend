from typing import Optional
from pydantic import BaseModel


class COPOMappingCreate(BaseModel):
    course_outcome_id: int
    program_outcome_id: int
    mapping_level: int


class COPOMappingUpdate(BaseModel):
    course_outcome_id: Optional[int] = None
    program_outcome_id: Optional[int] = None
    mapping_level: Optional[int] = None
    is_active: Optional[bool] = None


class COPOMappingResponse(BaseModel):
    id: int
    course_outcome_id: int
    program_outcome_id: int
    mapping_level: int
    is_active: bool

    class Config:
        from_attributes = True