from sqlalchemy.orm import Session
from core.entities.user import User
from core.repositories.user_repository import UserRepository

class UserRepositoryImpl(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, username: str, email: str, password_hash: str) -> User:
        user = User(username=username, email=email, password_hash=password_hash)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def update_user_balance(self, user_id: int, amount: int) -> bool:
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            user.balance += amount
            self.db.commit()
            return True
        return False