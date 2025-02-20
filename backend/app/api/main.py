from fastapi import APIRouter

from .routes import login, todos, user


api_router = APIRouter()

api_router.include_router(login.router, tags=["login"])
api_router.include_router(todos.router, tags=["todos"])
api_router.include_router(user.router, tags=["users"])
