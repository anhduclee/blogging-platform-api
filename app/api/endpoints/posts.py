from fastapi import APIRouter, Depends, Path, Query, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.crud import post as crud_post, comment as crud_comment
from app.api.dependencies import get_current_account
from app.models.account import Account, AccountRole
from app.models.post import PostCreate, PostUpdate, PostPublic, PostPublicWithAccount
from app.models.comment import CommentPublicWithAccount, CommentPublic, CommentCreate

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/", response_model=list[PostPublic])
async def read_posts(
    limit: int = Query(default=100, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session)
):
    posts = await crud_post.read_posts(session=session, limit=limit, offset=offset)
    return posts

@router.get("/{post_id}", response_model=PostPublicWithAccount)
async def read_post(post_id: int = Path(ge=1), session: AsyncSession = Depends(get_session)):
    post = await crud_post.read_post_account(session=session, post_id=post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return post

@router.post("/", response_model=PostPublic)
async def create_post(
    post_create: PostCreate,
    current_account: Account = Depends(get_current_account),
    session: AsyncSession = Depends(get_session)
):
    post = await crud_post.create_post(session=session, post_create=post_create, account=current_account)
    return post

@router.patch("/{post_id}", response_model=PostPublic)
async def edit_post(
    post_update: PostUpdate,
    post_id: int = Path(ge=1),
    current_account: Account = Depends(get_current_account),
    session: AsyncSession = Depends(get_session)
):
    post = await crud_post.read_post(session=session, post_id=post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if post.account_id != current_account.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    updated_post = await crud_post.update_post(session=session, post_update=post_update, post=post)
    return updated_post

@router.delete("/{post_id}")
async def delete_post(
    post_id: int = Path(ge=1),
    current_account: Account = Depends(get_current_account),
    session: AsyncSession = Depends(get_session)
):
    post = await crud_post.read_post(session=session, post_id=post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not (current_account.role == AccountRole.ADMIN or current_account.id == post.account_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await crud_post.delete_post(session=session, post=post)
    return {
        "message": "Post deleted"
    }

@router.get("/{post_id}/comments", response_model=list[CommentPublicWithAccount], tags=["comments"])
async def read_post_comments(post_id: int = Path(ge=1), session: AsyncSession = Depends(get_session)):
    post = await crud_post.read_post_comments(session=session, post_id=post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return post.comments

@router.post("/{post_id}/comments", response_model=CommentPublic, tags=["comments"])
async def create_comment(
    comment_create: CommentCreate,
    post_id: int = Path(ge=1),
    current_account: Account = Depends(get_current_account),
    session: AsyncSession = Depends(get_session)
):
    post = await crud_post.read_post(session=session, post_id=post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    comment = await crud_comment.create_comment(
        session=session,
        comment_create=comment_create,
        account=current_account,
        post=post
    )
    return comment