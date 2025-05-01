from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from infra.db.database import Base
from datetime import datetime

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # Must match User's __tablename__
    model_type = Column(String)
    input_data = Column(JSON)
    output_data = Column(JSON)
    cost = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)