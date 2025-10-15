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

def test_create_user(db_session):
    response = client.post(
        "/users/",
        json={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data

def test_login_for_access_token(db_session):
    # First, create a user to login with
    client.post(
        "/users/",
        json={"username": "testuser", "password": "testpassword"},
    )

    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data

def test_get_wallet(db_session):
    # Create a user and get a token
    client.post(
        "/users/",
        json={"username": "testuser", "password": "testpassword"},
    )
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpassword"},
    )
    token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/wallet/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert "btc_balance" in data
    assert "usd_balance" in data

def test_buy_btc(db_session, monkeypatch):
    # Mock the API call to return a fixed price
    async def mock_get_btc_price_usd():
        return 52000.0

    monkeypatch.setattr("app.api_client.get_btc_price_usd", mock_get_btc_price_usd)

    # Create a user and get a token
    client.post(
        "/users/",
        json={"username": "testuser", "password": "testpassword"},
    )
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpassword"},
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Get the wallet to check initial balance
    response = client.get("/wallet/", headers=headers)
    initial_usd_balance = response.json()["usd_balance"]
    initial_btc_balance = response.json()["btc_balance"]

    btc_to_buy = 1.0
    mock_price = 52000.0
    expected_usd_balance = initial_usd_balance - (btc_to_buy * mock_price)
    expected_btc_balance = initial_btc_balance + btc_to_buy

    response = client.post(
        f"/buy/?btc_amount={btc_to_buy}",
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["usd_balance"] == expected_usd_balance
    assert data["btc_balance"] == expected_btc_balance

def test_sell_btc(db_session, monkeypatch):
    # Mock the API call for both the initial buy and the sell
    async def mock_get_btc_price_for_buy():
        return 50000.0

    async def mock_get_btc_price_for_sell():
        return 53000.0

    # Create a user and get a token
    client.post(
        "/users/",
        json={"username": "testuser", "password": "testpassword"},
    )
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpassword"},
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Use monkeypatch for the buy transaction
    monkeypatch.setattr("app.api_client.get_btc_price_usd", mock_get_btc_price_for_buy)
    client.post(
        "/buy/?btc_amount=1",
        headers=headers,
    )

    # Get the wallet to check balance after buying
    response = client.get("/wallet/", headers=headers)
    balance_after_buy = response.json()
    initial_usd_balance = balance_after_buy["usd_balance"]
    initial_btc_balance = balance_after_buy["btc_balance"]

    # Use monkeypatch for the sell transaction
    monkeypatch.setattr("app.api_client.get_btc_price_usd", mock_get_btc_price_for_sell)

    btc_to_sell = 0.5
    mock_sell_price = 53000.0
    expected_usd_balance = initial_usd_balance + (btc_to_sell * mock_sell_price)
    expected_btc_balance = initial_btc_balance - btc_to_sell

    response = client.post(
        f"/sell/?btc_amount={btc_to_sell}",
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["usd_balance"] == expected_usd_balance
    assert data["btc_balance"] == expected_btc_balance

def test_get_transactions(db_session, monkeypatch):
    # Mock the API call
    async def mock_get_btc_price_usd():
        return 50000.0
    monkeypatch.setattr("app.api_client.get_btc_price_usd", mock_get_btc_price_usd)

    # Create a user, get a token, and make a transaction
    client.post(
        "/users/",
        json={"username": "testuser", "password": "testpassword"},
    )
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpassword"},
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    buy_response = client.post(
        "/buy/?btc_amount=1",
        headers=headers,
    )
    assert buy_response.status_code == 200

    response = client.get("/transactions/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["transaction_type"] == "buy"