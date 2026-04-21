from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.post import Post, PostCreate, PostUpdate
from app.models.account import Account
from app.models.comment import Comment

async def create_post(session: AsyncSession, post_create: PostCreate, account: Account):
    post = Post.model_validate(post_create)
    post.account = account
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post

async def read_posts(session: AsyncSession, limit: int, offset: int):
    posts = await session.exec(
        select(Post).offset(offset).limit(limit)
    )
    return posts.all()

async def read_post(session: AsyncSession, post_id: int):
    post = await session.get(Post, post_id)
    return post

async def update_post(session: AsyncSession, post_update: PostUpdate, post: Post):
    post_update_dict = post_update.model_dump(exclude_unset=True, exclude_none=True)
    post.sqlmodel_update(post_update_dict)
    session.add(post)
    await session.commit()
    return post

async def delete_post(session: AsyncSession, post: Post):
    await session.delete(post)
    await session.commit()
    return post

async def read_post_account(session: AsyncSession, post_id: int):
    post = await session.exec(
        select(Post).where(Post.id==post_id).options(selectinload(Post.account))
    )
    return post.first()

async def read_post_comments(session: AsyncSession, post_id: int):
    post = await session.exec(
        select(Post).where(Post.id==post_id).options(selectinload(Post.comments).selectinload(Comment.account))
    )
    return post.first()