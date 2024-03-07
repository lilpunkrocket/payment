from datetime import datetime
from sqlalchemy import String, TIMESTAMP, ForeignKey, DECIMAL
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Clients(Base):
    __tablename__ = 'clients'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(52))
    can_pay: Mapped[bool] = mapped_column(default=True)


class Transactions(Base):
    __tablename__ = 'transactions'
    id: Mapped[int] = mapped_column(primary_key=True)
    service: Mapped[str] = mapped_column(String(128), nullable=False)
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'))
    date: Mapped[datetime.timestamp] = mapped_column(
        TIMESTAMP, default=datetime.utcnow)
    bank: Mapped[str] = mapped_column(String(52), nullable=False)
    money_amount: Mapped[float] = mapped_column(DECIMAL, nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
