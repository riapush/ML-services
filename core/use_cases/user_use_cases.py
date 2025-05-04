from passlib.context import CryptContext
from core.entities.user import User
from core.repositories.user_repository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserUseCases:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_user(self, username: str, email: str, password: str) -> User:
        # Проверка существования пользователя
        if self.user_repo.get_user_by_email(email):
            raise ValueError("Email already registered")
        
        # Хеширование пароля
        password_hash = pwd_context.hash(password)
        
        # Создание пользователя
        return self.user_repo.create_user(username, email, password_hash)

    def authenticate_user(self, email: str, password: str) -> User:
        user = self.user_repo.get_user_by_email(email)
        if not user or not pwd_context.verify(password, user.password_hash):
            return None
        return user