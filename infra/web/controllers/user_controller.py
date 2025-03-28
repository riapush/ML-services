from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import timedelta
from infra.db.database import get_db
from core.entities.user import User
from core.use_cases.user_use_cases import UserUseCases
from infra.db.user_repository_impl import UserRepositoryImpl
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Модели запросов
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "yourpassword"
            }
        }

class Token(BaseModel):
    token: str
    token_type: str

# Эндпоинты
@router.post("/register")
def register(user_data: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user_repo = UserRepositoryImpl(db)
        
        # Проверка существования пользователя
        if user_repo.get_user_by_email(user_data.email):
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
        
        # Хеширование пароля
        password_hash = pwd_context.hash(user_data.password)
        
        # Создание пользователя
        user = user_repo.create_user(
            username=user_data.username,
            email=user_data.email,
            password_hash=password_hash
        )
        
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "balance": user.balance
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    try:
        user_repo = UserRepositoryImpl(db)
        user = user_repo.get_user_by_email(login_data.email)
        
        if not user or not pwd_context.verify(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=30)
        token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=access_token_expires
        )

        return {
            "token": token,
            "token_type": "bearer"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

# Функции аутентификации (перенесены сюда из main.py)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, "your-secret-key", algorithm="HS256")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = jwt.decode(token, "your-secret-key", algorithms=["HS256"])
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    user_repo = UserRepositoryImpl(db)
    user = user_repo.get_user_by_id(int(user_id))
    if user is None:
        raise credentials_exception
    return user

@router.get("/user")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/add_money")
def add_money(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        user_repo = UserRepositoryImpl(db)
        user_repo.update_user_balance(current_user.id, 50)
        db.refresh(current_user)
        return {"new_balance": current_user.balance}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))