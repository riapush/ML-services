from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Prediction(Base):
    __tablename__ = 'predictions'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    model_type = Column(String, nullable=False)
    input_data = Column(JSON, nullable=False)
    output_data = Column(JSON)
    cost = Column(Integer, nullable=False)

    def execute(self, model):
        self.output_data = model.predict(self.input_data)
        return self.output_data