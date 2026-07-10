from pydantic import BaseModel, EmailStr


class Register(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str
    department_id: int | None = None


class Login(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str