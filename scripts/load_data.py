import json
import sys
import os
import argparse
import logging
from sqlalchemy.exc import IntegrityError

# Add the parent directory to the Python path to allow importing from 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import SessionLocal, engine
from app.models import Question, Base

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(data_file: str):
    """
    Loads question data from a JSONL file into the database.

    Args:
        data_file (str): The path to the JSONL data file.
    """
    # Create tables
    logging.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logging.info("Database tables created.")

    db = SessionLocal()
    questions_added = 0

    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
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
                        questions_added += 1
                except json.JSONDecodeError:
                    logging.error(f"Error decoding JSON from line: {line.strip()}")
                except KeyError as e:
                    logging.error(f"Missing key {e} in line: {line.strip()}")

        db.commit()
        logging.info(f"Successfully added {questions_added} new questions.")

    except FileNotFoundError:
        logging.error(f"Data file not found at: {data_file}")
    except IntegrityError as e:
        logging.error(f"Database integrity error: {e}. Rolling back.")
        db.rollback()
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        db.rollback()
    finally:
        db.close()
        logging.info("Database session closed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load data into the quiz application database.")
    parser.add_argument(
        "--file",
        type=str,
        default="data/questions.jsonl",
        help="The path to the JSONL data file."
    )
    args = parser.parse_args()

    load_data(args.file)