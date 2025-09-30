import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models import Base, Question
from app.database import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_create_question(db_session):
    response = client.post(
        "/questions/",
        json={"question": "Test Question", "answer": "Test Answer", "topic": "Test Topic", "difficulty": "Easy"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["question"] == "Test Question"
    assert "id" in data

    db_question = db_session.query(Question).filter(Question.id == data["id"]).first()
    assert db_question is not None

def test_read_questions(db_session):
    question1 = Question(question="Q1", answer="A1", topic="T1", difficulty="Easy")
    question2 = Question(question="Q2", answer="A2", topic="T2", difficulty="Medium")
    db_session.add(question1)
    db_session.add(question2)
    db_session.commit()

    response = client.get("/questions/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["question"] == "Q1"
    assert data[1]["question"] == "Q2"

def test_read_question(db_session):
    question = Question(question="Test Question", answer="Test Answer", topic="Test", difficulty="Easy")
    db_session.add(question)
    db_session.commit()

    response = client.get(f"/questions/{question.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["question"] == "Test Question"

    response = client.get("/questions/999")
    assert response.status_code == 404

def test_update_question(db_session):
    question = Question(question="Old Question", answer="Old Answer", topic="Old", difficulty="Easy")
    db_session.add(question)
    db_session.commit()

    response = client.put(
        f"/questions/{question.id}",
        json={"question": "New Question", "answer": "New Answer", "topic": "New", "difficulty": "Hard"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["question"] == "New Question"
    assert data["difficulty"] == "Hard"

    db_session.refresh(question)
    assert question.question == "New Question"

def test_delete_question(db_session):
    question = Question(question="To Be Deleted", answer="Delete", topic="Delete", difficulty="Easy")
    db_session.add(question)
    db_session.commit()

    response = client.delete(f"/questions/{question.id}")
    assert response.status_code == 204

    db_question = db_session.query(Question).filter(Question.id == question.id).first()
    assert db_question is None

    response = client.delete("/questions/999")
    assert response.status_code == 404