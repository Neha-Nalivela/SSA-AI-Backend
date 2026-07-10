from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import Register
from app.utils.security import hash_password, verify_password
from app.utils.jwt_handler import create_access_token


class AuthService:

    @staticmethod
    def register(db: Session, data: Register):

        user = db.query(User).filter(
            User.email == data.email
        ).first()

        if user:
            raise Exception("Email already registered")

        new_user = User(
            name=data.name,
            email=data.email,
            password=hash_password(data.password),
            role=data.role,
            department_id=data.department_id
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    @staticmethod
    def login(db: Session, email: str, password: str):

        user = db.query(User).filter(
            User.email == email
        ).first()

        if not user:
            raise Exception("Invalid Email")

        if not verify_password(password, user.password):
            raise Exception("Invalid Password")

        token = create_access_token({
            "id": user.id,
            "email": user.email,
            "role": user.role
        })

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user
        }