from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import verify_password, create_access_token
from app.core.database import get_session
from app.crud.account import create_account, read_account
from app.models.account import AccountCreate, AccountPublic


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=AccountPublic)
async def register(account_create: AccountCreate, session: AsyncSession = Depends(get_session)):
    username = account_create.username
    db_account = await read_account(session=session, username=username)
    if db_account:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    account = await create_account(session=session, account_create=account_create)
    return account

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    username = form_data.username
    password = form_data.password
    account = await read_account(session=session, username=username)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not verify_password(password=password, hashed_password=account.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token(username=username)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }
