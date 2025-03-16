from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from core.use_cases.prediction_use_cases import PredictionUseCases
from infra.db.database import get_db
from infra.db.user_repository_impl import UserRepositoryImpl
from sqlalchemy.orm import Session

router = APIRouter()

class PredictionRequest(BaseModel):
    user_id: int
    model_type: str
    input_data: dict

@router.post("/predict")
def predict(prediction_data: PredictionRequest, db: Session = Depends(get_db)):
    user_repo = UserRepositoryImpl(db)
    prediction_uc = PredictionUseCases(user_repo)
    result = prediction_uc.make_prediction(prediction_data.user_id, prediction_data.model_type, prediction_data.input_data, cost=10)
    if not result:
        raise HTTPException(status_code=400, detail="Not enough credits")
    return {"result": result}