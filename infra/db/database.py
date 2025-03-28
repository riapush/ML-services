from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

# Настройка логирования
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

DATABASE_URL = "postgresql://postgres:admin@localhost:5432/postgres"

# Создаём Base
Base = declarative_base()

# После создания Base
Base = declarative_base()

# Явно импортируем и регистрируем модели
def register_models():
    from core.entities.user import User
    from core.entities.prediction import Prediction
    from core.entities.model import Model
    return [User, Prediction, Model]

models = register_models()

# Создаём engine
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()