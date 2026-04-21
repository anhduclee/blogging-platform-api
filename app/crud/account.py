from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.security import get_password_hash
from app.models.account import Account, AccountCreate, AccountRole, AccountUpdate
from app.models.comment import Comment

async def create_account(session: AsyncSession, account_create: AccountCreate, role: AccountRole = AccountRole.USER):
    update_data = {
        "hashed_password": get_password_hash(account_create.password),
        "role": role
    }
    account = Account.model_validate(account_create, update=update_data)
    session.add(account)
    await session.commit()
    return account

async def read_accounts(session: AsyncSession, limit: int, offset: int):
    accounts = await session.exec(
        select(Account).offset(offset).limit(limit)
    )
    return accounts.all()

async def read_account(session: AsyncSession, username: str):
    account = await session.exec(
        select(Account).where(Account.username == username)
    )
    return account.first()

async def update_account(session: AsyncSession, account: Account, account_update: AccountUpdate):
    account_update_dict = account_update.model_dump(exclude_unset=True, exclude_none=True)
    password = account_update_dict.get("password")
    if password:
        account_update_dict["hashed_password"] = get_password_hash(password)
    account.sqlmodel_update(account_update_dict)
    session.add(account)
    await session.commit()
    return account

async def delete_account(session: AsyncSession, account: Account):
    await session.delete(account)
    await session.commit()
    return account

async def read_account_posts(session: AsyncSession, username: str):
    account = await session.exec(
        select(Account).where(Account.username==username).options(selectinload(Account.posts))
    )
    return account.first()

async def read_account_comments(session: AsyncSession, username: str):
    account = await session.exec(
        select(Account).where(Account.username==username).options(selectinload(Account.comments).selectinload(Comment.post))
    )
    return account.first()