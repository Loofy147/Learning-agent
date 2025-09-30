from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

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

    db.delete(db_question)
    db.commit()
    return