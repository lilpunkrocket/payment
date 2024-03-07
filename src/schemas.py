from datetime import datetime
from pydantic import BaseModel


class ClientPost(BaseModel):
    id: int


class ClientGet(ClientPost):
    name: str


class TransactionPost(BaseModel):
    client_id: int
    bank: str
    service: str
    money_amount: float


class TransactionGet(TransactionPost):
    id: int
    status: str
    date: datetime


class TransactionOut(BaseModel):
    id: int
    client: str
    bank: str
    service: str
    date: datetime
    money_amount: float
    status: str
