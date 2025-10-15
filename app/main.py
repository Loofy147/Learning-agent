<<<<<< btc-trading-feature
from fastapi import FastAPI
=======
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import random
from typing import List

>>>>>> main
from . import models, database
from .routers import trading, questions

app = FastAPI()

<<<<<< btc-trading-feature
@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=database.engine)
=======
@app.post("/questions/", response_model=models.QuestionResponse)
def create_question(question: models.QuestionCreate, db: Session = Depends(database.get_db)):
    db_question = models.Question(**question.model_dump())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@app.get("/questions/{question_id}", response_model=models.QuestionResponse)
def read_question(question_id: int, db: Session = Depends(database.get_db)):
    db_question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question

@app.get("/questions/", response_model=List[models.QuestionResponse])
def read_questions(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    questions = db.query(models.Question).offset(skip).limit(limit).all()
    return questions

@app.get("/questions/random/", response_model=models.QuestionResponse)
def read_random_question(db: Session = Depends(database.get_db)):
    question_ids = db.query(models.Question.id).all()
    if not question_ids:
        raise HTTPException(status_code=404, detail="No questions found")
    random_id = random.choice(question_ids)[0]
    random_question = db.query(models.Question).filter(models.Question.id == random_id).first()
    return random_question

@app.get("/questions/search/", response_model=List[models.QuestionResponse])
def search_questions(topic: str, skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    questions = db.query(models.Question).filter(models.Question.topic.ilike(f"%{topic}%")).offset(skip).limit(limit).all()
    return questions

@app.put("/questions/{question_id}", response_model=models.QuestionResponse)
def update_question(question_id: int, question: models.QuestionCreate, db: Session = Depends(database.get_db)):
    db_question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    for key, value in question.model_dump().items():
        setattr(db_question, key, value)

    db.commit()
    db.refresh(db_question)
    return db_question

@app.delete("/questions/{question_id}", status_code=204)
def delete_question(question_id: int, db: Session = Depends(database.get_db)):
    db_question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
>>>>>> main

app.include_router(trading.router)
app.include_router(questions.router)
