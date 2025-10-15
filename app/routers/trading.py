from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from .. import models, database, security, auth, api_client, schemas

router = APIRouter()

@router.post("/token", response_model=auth.Token)
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

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
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

@router.get("/wallet/", response_model=schemas.Wallet)
def get_wallet(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    db_wallet = db.query(models.Wallet).filter(models.Wallet.user_id == current_user.id).first()
    if db_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return db_wallet

@router.post("/buy/")
async def buy_btc(btc_amount: float, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    db_wallet = db.query(models.Wallet).filter(models.Wallet.user_id == current_user.id).first()
    if db_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")

    btc_price_usd = await api_client.get_btc_price_usd()
    usd_to_spend = btc_amount * btc_price_usd

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

@router.post("/sell/")
async def sell_btc(btc_amount: float, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    db_wallet = db.query(models.Wallet).filter(models.Wallet.user_id == current_user.id).first()
    if db_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")

    if db_wallet.btc_balance < btc_amount:
        raise HTTPException(status_code=400, detail="Insufficient BTC balance")

    btc_price_usd = await api_client.get_btc_price_usd()
    usd_to_gain = btc_amount * btc_price_usd

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

@router.get("/transactions/", response_model=List[schemas.Transaction])
def get_transactions(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    db_wallet = db.query(models.Wallet).filter(models.Wallet.user_id == current_user.id).first()
    if db_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    transactions = db.query(models.Transaction).filter(models.Transaction.wallet_id == db_wallet.id).all()
    return transactions
