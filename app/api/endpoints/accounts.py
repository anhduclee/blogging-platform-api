from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.api.dependencies import RoleChecker
from app.models.account import Account, AccountRole, AccountPublic
from app.models.post import PostPublic
from app.models.comment import CommentPublicWithPost
from app.crud import account as crud_account

router = APIRouter(prefix="/accounts", tags=["accounts"])
    
@router.get("/", response_model=list[AccountPublic])
async def read_accounts(
    limit: int = Query(default=100, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current_account: Account = Depends(RoleChecker([AccountRole.ADMIN])),
    session: AsyncSession = Depends(get_session)
):
    accounts = await crud_account.read_accounts(session=session, limit=limit, offset=offset)
    return accounts

@router.get("/{username}", response_model=AccountPublic)
async def read_account(username: str = Path(min_length=1), session: AsyncSession = Depends(get_session)):
    account = await crud_account.read_account(session=session, username=username)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return account

@router.delete("/{username}")
async def delete_account(
    current_account: Account = Depends(RoleChecker([AccountRole.ADMIN])),
    username: str = Path(min_length=1),
    session: AsyncSession = Depends(get_session)
):
    account = await crud_account.read_account(session=session, username=username)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await crud_account.delete_account(session=session, account=account)
    return {
        "message": "Account deleted"
    }

@router.get("/{username}/posts", response_model=list[PostPublic])
async def read_account_posts(username: str = Path(min_length=1), session: AsyncSession = Depends(get_session)):
    account = await crud_account.read_account_posts(session=session, username=username)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    posts = account.posts
    return posts

@router.get("/{username}/comments", response_model=list[CommentPublicWithPost])
async def read_account_comments(username: str = Path(min_length=1), session: AsyncSession = Depends(get_session)):
    account = await crud_account.read_account_comments(session=session, username=username)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    comments = account.comments
    return comments
