from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.post("/questions/", response_model=models.QuestionResponse)
def create_question(question: models.QuestionCreate, db: Session = Depends(database.get_db)):
    db_question = models.Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@app.get("/questions/", response_model=List[models.QuestionResponse])
def read_questions(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    questions = db.query(models.Question).offset(skip).limit(limit).all()
    return questions
