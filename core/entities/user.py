from sqlalchemy import Column, Integer, String
from infra.db.database import Base

class User(Base):
    __tablename__ = "users"  # Must match exactly
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
    balance = Column(Integer, default=0)