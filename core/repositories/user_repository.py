from abc import ABC, abstractmethod
from typing import Optional
from core.entities.prediction import Prediction
from core.entities.user import User

class UserRepository(ABC):
    @abstractmethod
    def create_user(self, username: str, email: str, password_hash: str) -> User:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def update_user_balance(self, user_id: int, amount: int) -> bool:
        pass

    @abstractmethod
    def save_prediction(self, prediction: Prediction) -> int:
        pass