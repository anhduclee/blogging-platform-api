from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.api import api_router
from app.core.config import settings
from app.core.database import init_db, drop_db, async_session
from app.crud.account import create_account
from app.models.account import AccountCreate, AccountRole

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    async with async_session() as session:
        admin = AccountCreate(
            username=settings.ADMIN_USERNAME,
            password=settings.ADMIN_PASSWORD
        )
        await create_account(session=session, account_create=admin, role=AccountRole.ADMIN)
    yield
    await drop_db()

app = FastAPI(lifespan=lifespan)
app.include_router(api_router)

@app.get("/ping")
async def ping():
    return {"ping": "pong"}