from passlib.context import CryptContext
from core.entities.user import User
from core.repositories.user_repository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserUseCases:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_user(self, username: str, email: str, password: str) -> User:
        password_hash = pwd_context.hash(password)
        return self.user_repo.create_user(username, email, password_hash)

    def authenticate_user(self, email: str, password: str) -> User:
        user = self.user_repo.get_user_by_email(email)
        if user and user.verify_password(password, pwd_context):
            return user
        return None