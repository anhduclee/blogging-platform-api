from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.crud.account import read_account, update_account, delete_account
from app.models.account import Account, AccountPublic, AccountUpdate
from app.api.dependencies import get_current_account

router = APIRouter(prefix="/me", tags=["me"])

@router.get("/", response_model=AccountPublic)
async def read_me(current_account: AsyncSession = Depends(get_current_account)):
    return current_account

@router.patch("/", response_model=AccountUpdate)
async def update_me(
    account_update: AccountUpdate,
    current_account: Account = Depends(get_current_account),
    session: AsyncSession = Depends(get_session)
):
    db_account = await read_account(session=session, username=account_update.username)
    if db_account:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    account = await update_account(session=session, account=current_account, account_update=account_update)
    return account

@router.delete("/")
async def delete_me(
    current_account: Account = Depends(get_current_account),
    session: AsyncSession = Depends(get_session)
):
    await delete_account(session=session, account=current_account)
    return {
        "message": "Account deleted"
    }