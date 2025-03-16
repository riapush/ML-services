from core.entities.model import Model
from core.entities.prediction import Prediction
from core.entities.user import User
from core.repositories.user_repository import UserRepository

class PredictionUseCases:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def make_prediction(self, user_id: int, model_type: str, input_data: dict, cost: int) -> dict:
        user = self.user_repo.get_user_by_id(user_id)
        if user and user.deduct_credits(cost):
            prediction = Prediction(user_id=user_id, model_type=model_type, input_data=input_data, cost=cost)
            model = self._get_model(model_type)
            output_data = prediction.execute(model)
            return output_data
        return None

    def _get_model(self, model_type: str):
        # Заглушка для получения модели
        return Model(type=model_type, cost=10)