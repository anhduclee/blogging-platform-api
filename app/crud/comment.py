from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.account import Account
from app.models.post import Post
from app.models.comment import Comment, CommentCreate, CommentUpdate

async def create_comment(session: AsyncSession, comment_create: CommentCreate, account: Account, post: Post):
    comment = Comment.model_validate(comment_create)
    comment.account = account
    comment.post = post
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    return comment

async def read_comments(session: AsyncSession, limit: int, offset: int):
    comments = await session.exec(
        select(Comment).offset(offset).limit(limit)
    )
    return comments.all()

async def read_comment(session: AsyncSession, comment_id: int):
    comment = await session.get(Comment, comment_id)
    return comment

async def update_comment(session: AsyncSession, comment_update: CommentUpdate, comment: Comment):
    comment_update_dict = comment_update.model_dump(exclude_unset=True, exclude_none=True)
    comment.sqlmodel_update(comment_update_dict)
    session.add(comment)
    await session.commit()
    return comment

async def delete_comment(session: AsyncSession, comment: Comment):
    await session.delete(comment)
    await session.commit()
    return comment

async def read_comment_with_account_and_post(comment_id: int, session: AsyncSession):
    comment = await session.exec(
        select(Comment).where(Comment.id==comment_id).options(selectinload(Comment.account), selectinload(Comment.post))
    )
    return comment.first()