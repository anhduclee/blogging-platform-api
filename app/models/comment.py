from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.account import Account, AccountPublic
    from app.models.post import Post, PostPublic

class Comment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    body: str
    account_id: int | None = Field(default=None, foreign_key="account.id", ondelete="CASCADE")
    post_id: int | None = Field(default=None, foreign_key="post.id", ondelete="CASCADE")
    account: "Account" = Relationship(back_populates="comments")
    post: "Post" = Relationship(back_populates="comments")

class CommentCreate(SQLModel):
    body: str = Field(min_length=1)

class CommentUpdate(SQLModel):
    body: str = Field(min_length=1)

class CommentPublic(SQLModel):
    id: int
    body: str

class CommentPublicWithAccount(SQLModel):
    id: int
    body: str
    account: "AccountPublic"

class CommentPublicWithPost(SQLModel):
    id: int
    body: str
    post: "PostPublic"

class CommentPublicWithAccountAndPost(SQLModel):
    id: int
    body: str
    account: "AccountPublic"
    post: "PostPublic"