from fastapi import APIRouter

from .routes import auth, todos, user


api_router = APIRouter()

api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(todos.router, tags=["todos"])
api_router.include_router(user.router, tags=["users"])
