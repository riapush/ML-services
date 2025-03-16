from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from core.use_cases.user_use_cases import UserUseCases
from infra.db.database import get_db
from infra.db.user_repository_impl import UserRepositoryImpl
from sqlalchemy.orm import Session

router = APIRouter()

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(user_data: RegisterRequest, db: Session = Depends(get_db)):
    user_repo = UserRepositoryImpl(db)
    user_uc = UserUseCases(user_repo)
    user = user_uc.register_user(user_data.username, user_data.email, user_data.password)
    return {"id": user.id, "username": user.username, "email": user.email}

@router.post("/login")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user_repo = UserRepositoryImpl(db)
    user_uc = UserUseCases(user_repo)
    user = user_uc.authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Logged in successfully"}