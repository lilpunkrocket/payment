import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from random import choice

from .models import Clients, Transactions
from .schemas import TransactionPost

API = None
PAY_API = None


async def check_client(id: int) -> bool:
    if not API:
        return choice((True, True, True, True, False))  # plug

    async with aiohttp.ClientSession() as session:
        try:
            # In this case, let's assume that the server returns the status code 200 if the client is not blacklisted
            async with session.get(f"{API}/{id}", timeout=aiohttp.ClientTimeout(total=15)) as resp:
                return resp.status == 200
        except:
            return False


async def pay(transaction: Transactions) -> bool:
    if not PAY_API:
        return choice((True, True, True, True, False))  # plug

    async with aiohttp.ClientSession() as session:
        try:
            # In this case, let's assume that the server returns the status code 200 if the transaction was succesfull
            async with session.post(f"{API}/", timeout=aiohttp.ClientTimeout(total=15), data={
                {'client_id'}: transaction.client_id,
                {'transaction_id'}: transaction.id,
            }) as resp:
                return resp.status == 200
        except:
            return False


async def do_transaction(db: AsyncSession, client: Clients, transaction: TransactionPost) -> Transactions:
    client.can_pay = client.can_pay and await check_client(client.id)
    new_transaction = Transactions(client_id=client.id, bank=transaction.bank,
                                   service=transaction.service, money_amount=transaction.money_amount, status=('FAILED', 'SUCCES')[client.can_pay])

    db.add(new_transaction)

    await db.commit()
    await db.refresh(client)
    await db.refresh(new_transaction)

    if not client.can_pay:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail=f'Client with id = {client.id} is blocked')
    
    transaction_succes_status = await pay(new_transaction)

    if not transaction_succes_status:
        new_transaction.status = 'FAILED'
        await db.commit()
        await db.refresh(new_transaction)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Transaction with id = {new_transaction.id} failed')

    return new_transaction
