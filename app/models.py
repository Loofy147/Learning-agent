from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

DATABASE_URL = "sqlite:///./test.db"

Base = declarative_base()

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

    class Config:
        from_attributes = True
