from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.account import Account, AccountPublic
    from app.models.comment import Comment, CommentPublic

class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    body: str
    account_id: int | None = Field(default=None, foreign_key="account.id", ondelete="CASCADE")
    account: "Account" = Relationship(back_populates="posts")
    comments: list["Comment"] = Relationship(back_populates="post", passive_deletes=True)

class PostCreate(SQLModel):
    title: str = Field(min_length=1)
    body: str = Field(min_length=1)

class PostUpdate(SQLModel):
    title: str | None = None
    body: str | None = None

class PostPublic(SQLModel):
    id: int
    title: str
    body: str

class PostPublicWithAccount(SQLModel):
    id: int
    title: str
    body: str
    account: "AccountPublic"

class PostPublicWithComments(SQLModel):
    id: int
    title: str
    body: str
    comments: list["CommentPublic"] = Field(default_factory=list)

class PostPublicWithAccountAndComments(SQLModel):
    id: int
    title: str
    body: str
    account: "AccountPublic"
    comments: list["CommentPublic"] = Field(default_factory=list)