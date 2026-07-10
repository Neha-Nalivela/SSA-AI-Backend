from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import Register
from app.services.auth_service import AuthService
from app.dependencies.auth import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)
@router.post("/register")
def register(
    data: Register,
    db: Session = Depends(get_db)
):
    try:
        return AuthService.register(db, data)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    try:
        return AuthService.login(
            db, 
            form_data.username,
            form_data.password)
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )
@router.get("/me")
def me(
    current_user=Depends(get_current_user)
):

    return current_user