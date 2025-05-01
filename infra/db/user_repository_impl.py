from sqlalchemy.orm import Session
from core.entities.user import User
from core.repositories.user_repository import UserRepository
from passlib.context import CryptContext
from core.entities.prediction import Prediction

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepositoryImpl(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, username: str, email: str, password_hash: str) -> User:
        try:
            user = User(
                username=username,
                email=email,
                password_hash=password_hash,
                balance=0
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Database error: {str(e)}")

    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    def update_user_balance(self, user_id: int, amount: int) -> bool:
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if user:
                user.balance += amount  # Direct balance update
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Database error: {str(e)}")
        
    def get_user_predictions(self, user_id: int):
        return self.db.query(Prediction)\
            .filter(Prediction.user_id == user_id)\
            .order_by(Prediction.created_at.desc())\
            .all()
    
    def save_prediction(self, prediction: Prediction) -> int:
        try:
            self.db.add(prediction)
            self.db.commit()
            self.db.refresh(prediction)
            return prediction.id
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Failed to save prediction: {str(e)}")