from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    wallets = relationship("Wallet", back_populates="owner")

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    btc_balance = Column(Float, default=0.0)
    usd_balance = Column(Float, default=100000.0)

    owner = relationship("User", back_populates="wallets")
    transactions = relationship("Transaction", back_populates="wallet")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"))
    transaction_type = Column(String)
    btc_amount = Column(Float)
    usd_amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    wallet = relationship("Wallet", back_populates="transactions")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, index=True)
    answer = Column(Text)
    topic = Column(String, index=True)
    difficulty = Column(String)

class QuestionCreate(BaseModel):
    question: str
    answer: str
    topic: str
    difficulty: str

class QuestionResponse(QuestionCreate):
    id: int

    model_config = {"from_attributes": True}

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    model_config = {"from_attributes": True}

class WalletResponse(BaseModel):
    id: int
    user_id: int
    btc_balance: float
    usd_balance: float

    model_config = {"from_attributes": True}

class TransactionCreate(BaseModel):
    transaction_type: str
    btc_amount: float
    usd_amount: float

class TransactionResponse(TransactionCreate):
    id: int
    wallet_id: int
    timestamp: datetime.datetime

    model_config = {"from_attributes": True}
