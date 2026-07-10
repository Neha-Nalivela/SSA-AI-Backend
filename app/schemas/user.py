from pydantic import BaseModel
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    department_id: int | None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True