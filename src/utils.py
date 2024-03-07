from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Transactions, Clients, Base


async def create_or_find(db: AsyncSession, model: Base, id: int, name: str = None) -> Base:
    query = select(model).where(model.id == id)
    result = await db.execute(query)
    obj = result.scalar_one_or_none()
    if obj:
        return obj

    if not name:
        name = "Unknown " + model.__name__.removesuffix('s')

    new_obj = model(id=id, name=name)
    db.add(new_obj)
    await db.commit()
    await db.refresh(new_obj)
    return new_obj


async def get_transaction(db: AsyncSession, id: int):
    query = select(Transactions.id, Transactions.date, Transactions.bank, Transactions.service, Transactions.status, Transactions.money_amount, Clients.name.label('client')).join(
        Clients, Transactions.client_id == Clients.id).where(Transactions.id == id)
    result = await db.execute(query)
    transaction = result.first()
    return transaction
