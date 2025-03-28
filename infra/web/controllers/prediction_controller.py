from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from core.use_cases.prediction_use_cases import PredictionUseCases
from infra.db.user_repository_impl import UserRepositoryImpl
from infra.db.database import get_db
from sqlalchemy.orm import Session
from fastapi import Query
from .user_controller import get_current_user
from core.entities.prediction import Prediction  # Add this import
from core.entities.user import User  # Ensure this exists
from infra.db.user_repository_impl import UserRepositoryImpl

router = APIRouter()

class PredictionRequest(BaseModel):
    model_type: str  # "cheap", "medium" or "expensive"
    input_data: dict  # Prediction data

class PredictionResponse(BaseModel):
    prediction_id: int
    result: dict
    cost: int
    remaining_balance: int

@router.post("/predict", response_model=PredictionResponse)
def make_prediction(
    request: PredictionRequest,
    current_user: User = Depends(get_current_user),  # Add auth dependency
    db: Session = Depends(get_db)
):
    user_repo = UserRepositoryImpl(db)
    prediction_uc = PredictionUseCases(user_repo)
    
    try:
        # Use the authenticated user's ID
        result = prediction_uc.make_prediction(
            user_id=current_user.id,  # Use authenticated user's ID
            model_type=request.model_type,
            input_data=request.input_data
        )
        
        # Refresh user balance
        db.refresh(current_user)
        
        return {
            "prediction_id": result["prediction_id"],
            "result": result["output"],
            "cost": result["cost"],
            "remaining_balance": current_user.balance
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/predictions_history")
async def get_prediction_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print(f"Current user ID: {current_user.id if current_user else 'None'}")  # Debug
    
    try:
        user_repo = UserRepositoryImpl(db)
        prediction_uc = PredictionUseCases(user_repo)
        predictions = prediction_uc.get_user_predictions(current_user.id)
        
        print(f"Found {len(predictions)} predictions")  # Debug
        return {"predictions": predictions}
        
    except Exception as e:
        print(f"Error in predictions_history: {str(e)}")  # Detailed error
        raise HTTPException(
            status_code=400,
            detail=str(e))