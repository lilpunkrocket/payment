from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException as StarletteHTTPException
from logger.core import init_tables
from src.core import check_client, do_transaction
from src.exceptions import http_exception_handler
from src.middlewares import LogMiddleWare
from src.utils import create_or_find, get_transaction
from src.database import get_db
from src import schemas
from src.models import Transactions, Clients


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(LogMiddleWare)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)


@app.get('/payment/{id}', response_model=schemas.TransactionOut)
async def index(id: int, db: AsyncSession = Depends(get_db)):
    transaction = await get_transaction(db=db, id=id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'There are not transaction with id = {id}')
    return transaction


@app.post('/payment', status_code=status.HTTP_201_CREATED, response_model=schemas.TransactionGet)
async def index(transaction: schemas.TransactionPost, db: AsyncSession = Depends(get_db)):
    client = await create_or_find(db=db, model=Clients, id=transaction.client_id)
    return await do_transaction(db=db, transaction=transaction, client=client)
