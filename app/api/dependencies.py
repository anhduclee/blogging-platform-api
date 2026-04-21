from fastapi import Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.core.security import decode_access_token, oauth2_scheme
from app.crud.account import read_account
from app.models.account import Account, AccountRole

async def get_current_account(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )
    username = decode_access_token(token=token)
    if not username:
        raise credentials_exception
    account = await read_account(session=session, username=username)
    if not account:
        raise credentials_exception
    return account

class RoleChecker():
    def __init__(self, allowed_roles: list[AccountRole]):
        self.allowed_roles = allowed_roles
    def __call__(self, current_account: Account = Depends(get_current_account)):
        if current_account.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN
            )
        return current_account