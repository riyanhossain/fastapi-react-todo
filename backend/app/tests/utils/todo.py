from sqlalchemy.ext.asyncio import AsyncSession
from random import choice

from app import crud, schemas
from .user import create_random_user

from .utils import random_lower_string


def get_random_todo_status():
    return choice(["todo", "completed", "in_progress"])


def get_random_todo_priority():
    return choice(["low", "medium", "high"])


async def create_random_todo(db: AsyncSession):
    user_obj = await create_random_user(db)
    user = user_obj["data"]
    title = random_lower_string()
    content = random_lower_string()
    status = get_random_todo_status()
    priority = get_random_todo_priority()

    todo_data = schemas.TodoCreate(
        title=title,
        content=content,
        status=schemas.TodoStatus(status),
        priority=schemas.TodoPriority(priority),
    )

    # Fix: Change user.id to user["id"] for dictionary access
    todo = await crud.create_todo(db, todo_data, user_id=str(user["id"]))
    return {"user": user_obj, "todo": todo}
