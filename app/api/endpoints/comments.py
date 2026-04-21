from fastapi import APIRouter, Depends, Path, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.account import Account, AccountRole
from app.models.comment import CommentUpdate, CommentPublic, CommentPublicWithAccountAndPost
from app.core.database import get_session
from app.api.dependencies import get_current_account
from app.crud import comment as crud_comment

router = APIRouter(prefix="/comments", tags=["comments"])

@router.get("/{comment_id}", response_model=CommentPublicWithAccountAndPost)
async def read_comment(
    comment_id: int = Path(ge=1),
    session: AsyncSession = Depends(get_session)
):
    comment = await crud_comment.read_comment_with_account_and_post(comment_id=comment_id, session=session)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return comment

@router.patch("/{comment_id}", response_model=CommentPublic)
async def update_comment(
    comment_update: CommentUpdate,
    comment_id: int = Path(ge=1),
    current_account: Account = Depends(get_current_account),
    session: AsyncSession = Depends(get_session)
):
    comment = await crud_comment.read_comment(session=session, comment_id=comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if comment.account_id != current_account.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    updated_comment = await crud_comment.update_comment(
        session=session,
        comment_update=comment_update,
        comment=comment
    )
    return updated_comment

@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int = Path(ge=1),
    current_account: Account = Depends(get_current_account),
    session: AsyncSession = Depends(get_session)
):
    comment = await crud_comment.read_comment(session=session, comment_id=comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not (comment.account_id == current_account.id or current_account.role == AccountRole.ADMIN):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await crud_comment.delete_comment(session=session, comment=comment)
    return {
        "message": "Comment deleted"
    }