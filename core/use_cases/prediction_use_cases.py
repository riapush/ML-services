from datetime import datetime
from core.entities.prediction import Prediction
from core.repositories.user_repository import UserRepository
from core.entities.model import CheapModel, MediumModel, ExpensiveModel, BaseModel

class PredictionUseCases:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def _get_model(self, model_type: str) -> BaseModel:
        models = {
            "cheap": CheapModel(),
            "medium": MediumModel(),
            "expensive": ExpensiveModel()
        }
        return models.get(model_type)

    def _execute_prediction(self, model: BaseModel, input_data: dict) -> dict:
        print('model.predict(input_data)', model.predict(input_data))
        return model.predict(input_data)

    def make_prediction(self, user_id: int, model_type: str, input_data: dict):
        model = self._get_model(model_type)
        if not model:
            raise ValueError("Invalid model type")
            
        # Rest of the logic remains similar
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
            
        if user.balance < model.cost:
            raise ValueError("Not enough credits")

        # Deduct credits
        self.user_repo.update_user_balance(user_id, -model.cost)

        # Create prediction
        prediction = Prediction(
            user_id=user_id,
            model_type=model_type,
            input_data=input_data,
            cost=model.cost,
            created_at=datetime.now(),
            output_data=self._execute_prediction(model, input_data['data'])
        )

        prediction_id = self.user_repo.save_prediction(prediction)
        
        return {
            "prediction_id": prediction_id,
            "output": prediction.output_data,
            "cost": model.cost
        }
    
    def get_user_predictions(self, user_id: int) -> list:
        """Retrieve all predictions for a user."""
        predictions = self.user_repo.get_user_predictions(user_id)
        return [
            {
                "id": p.id,
                "model_type": p.model_type,
                "input_data": p.input_data,
                "output_data": p.output_data,
                "cost": p.cost,
                "created_at": p.created_at.isoformat()
            }
            for p in predictions
        ]