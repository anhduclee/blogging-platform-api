from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from enum import StrEnum

if TYPE_CHECKING:
    from app.models.post import Post, PostPublic
    from app.models.comment import Comment, CommentPublic

class AccountRole(StrEnum):
    ADMIN = "admin"
    USER = "user"

class Account(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    role: AccountRole = AccountRole.USER
    posts: list["Post"] = Relationship(back_populates="account", passive_deletes=True)
    comments: list["Comment"] = Relationship(back_populates="account", passive_deletes=True)

class AccountCreate(SQLModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)

class AccountUpdate(SQLModel):
    username: str | None = None
    password: str | None = None

class AccountPublic(SQLModel):
    username: str

class AccountPublicWithPosts(SQLModel):
    username: str
    posts: list["PostPublic"] = Field(default_factory=list)

class AccountPublicWithComments(SQLModel):
    username: str
    comments: list["CommentPublic"] = Field(default_factory=list)

class AccountPublicWithPostsAndComments(SQLModel):
    username: str
    posts: list["PostPublic"] = Field(default_factory=list)
    comments: list["CommentPublic"] = Field(default_factory=list)