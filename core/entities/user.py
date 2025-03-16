from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    balance = Column(Integer, default=0)

    def deduct_credits(self, amount: int):
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False

    def add_credits(self, amount: int):
        self.balance += amount

    def verify_password(self, password: str, pwd_context):
        return pwd_context.verify(password, self.password_hash)