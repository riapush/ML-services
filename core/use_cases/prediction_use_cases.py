from datetime import datetime
from core.entities.prediction import Prediction
from core.repositories.user_repository import UserRepository
from core.entities.model import Model

class PredictionUseCases:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def make_prediction(self, user_id: int, model_type: str, input_data: dict):
        model = self._get_model(model_type)
        user = self.user_repo.get_user_by_id(user_id)
        
        if not user:
            raise ValueError("User not found")
        if user.balance < model.cost:
            raise ValueError("Not enough credits")

        # Update balance through repository method instead of user object
        if not self.user_repo.update_user_balance(user_id, -model.cost):
            raise ValueError("Balance update failed")

        # Create and save prediction
        prediction = Prediction(
            user_id=user_id,
            model_type=model_type,
            input_data=input_data,
            cost=model.cost,
            created_at=datetime.now()
        )
        
        prediction.output_data = self._execute_prediction(model, input_data)
        prediction_id = self.user_repo.save_prediction(prediction)
        
        return {
            "prediction_id": prediction_id,
            "output": prediction.output_data,
            "cost": model.cost
        }
    
    def _get_model(self, model_type: str):
        models = {
            "cheap": Model(type="cheap", cost=10),
            "medium": Model(type="medium", cost=20),
            "expensive": Model(type="expensive", cost=50)
        }
        return models.get(model_type)
    
    def _execute_prediction(self, model, input_data):
        # Здесь будет реальная логика предсказания
        # Пока используем заглушку
        return {
            "prediction": f"Result from {model.type} model",
            "confidence": 0,
            "input_processed": input_data
        }
    
    def get_user_predictions(self, user_id: int):
        predictions = self.user_repo.get_user_predictions(user_id)
        return [
            {
                "id": p.id,
                "model_type": p.model_type,
                "cost": p.cost,
                "created_at": p.created_at.isoformat(),
                "input_data": p.input_data,
                "output_data": p.output_data
            }
            for p in predictions
        ]