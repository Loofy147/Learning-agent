from pydantic import BaseModel

class QuestionBase(BaseModel):
    question: str
    answer: str
    topic: str
    difficulty: str

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int

    class Config:
        orm_mode = True
