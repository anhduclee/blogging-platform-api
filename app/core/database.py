from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models.account import Account
from app.models.post import Post
from app.models.comment import Comment

engine = create_async_engine(url=settings.DB_URL, echo=True, future=True)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

async def get_session():
    async with async_session() as session:
        yield session