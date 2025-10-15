from pydantic import BaseModel
import datetime

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    order_type: str
    btc_amount: float
    price_usd: float

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    wallet_id: int
    is_active: bool
    timestamp: datetime.datetime

    class Config:
        orm_mode = True

class WalletBase(BaseModel):
    btc_balance: float
    usd_balance: float

class Wallet(WalletBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class TransactionBase(BaseModel):
    transaction_type: str
    btc_amount: float
    usd_amount: float

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    wallet_id: int
    timestamp: datetime.datetime

    class Config:
        orm_mode = True
