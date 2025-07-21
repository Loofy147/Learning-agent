import json
import sys
import os

# Add the parent directory to the Python path to allow importing from 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import SessionLocal, engine
from app.models import Question, Base

def load_data():
    # Create tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    with open('data/questions.jsonl', 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            question = db.query(Question).filter(Question.id == data['id']).first()
            if not question:
                db_question = Question(
                    id=data['id'],
                    question=data['question'],
                    answer=data['answer'],
                    topic=data['topic'],
                    difficulty=data['difficulty']
                )
                db.add(db_question)

    db.commit()
    db.close()
    print("Data loaded successfully.")

if __name__ == "__main__":
    load_data()
