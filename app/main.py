from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from . import models, database, security, auth

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.post("/token", response_model=auth.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=models.UserResponse)
def create_user(user: models.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Create a wallet for the new user
    db_wallet = models.Wallet(user_id=db_user.id)
    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)

    return db_user

@app.get("/wallet/", response_model=models.WalletResponse)
def get_wallet(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    db_wallet = db.query(models.Wallet).filter(models.Wallet.user_id == current_user.id).first()
    if db_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return db_wallet

@app.post("/buy/")
def buy_btc(btc_amount: float, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    db_wallet = db.query(models.Wallet).filter(models.Wallet.user_id == current_user.id).first()
    if db_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")

    # This is a mock price for BTC
    usd_to_spend = btc_amount * auth.settings.BTC_PRICE_USD

    if db_wallet.usd_balance < usd_to_spend:
        raise HTTPException(status_code=400, detail="Insufficient USD balance")

    db_wallet.usd_balance -= usd_to_spend
    db_wallet.btc_balance += btc_amount

    transaction = models.Transaction(
        wallet_id=db_wallet.id,
        transaction_type="buy",
        btc_amount=btc_amount,
        usd_amount=usd_to_spend,
    )
    db.add(transaction)
    db.commit()
    db.refresh(db_wallet)
    return db_wallet

@app.post("/sell/")
def sell_btc(btc_amount: float, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    db_wallet = db.query(models.Wallet).filter(models.Wallet.user_id == current_user.id).first()
    if db_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")

    if db_wallet.btc_balance < btc_amount:
        raise HTTPException(status_code=400, detail="Insufficient BTC balance")

    # This is a mock price for BTC
    usd_to_gain = btc_amount * auth.settings.BTC_PRICE_USD

    db_wallet.btc_balance -= btc_amount
    db_wallet.usd_balance += usd_to_gain

    transaction = models.Transaction(
        wallet_id=db_wallet.id,
        transaction_type="sell",
        btc_amount=btc_amount,
        usd_amount=usd_to_gain,
    )
    db.add(transaction)
    db.commit()
    db.refresh(db_wallet)
    return db_wallet

@app.get("/transactions/", response_model=List[models.TransactionResponse])
def get_transactions(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    db_wallet = db.query(models.Wallet).filter(models.Wallet.user_id == current_user.id).first()
    if db_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    transactions = db.query(models.Transaction).filter(models.Transaction.wallet_id == db_wallet.id).all()
    return transactions

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