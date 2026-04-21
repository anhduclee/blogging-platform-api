from fastapi import APIRouter
from app.api.endpoints import auth, me, accounts, posts, comments

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(me.router)
api_router.include_router(accounts.router)
api_router.include_router(posts.router)
api_router.include_router(comments.router)