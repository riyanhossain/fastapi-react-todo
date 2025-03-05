# from sqlalchemy.ext.asyncio import AsyncSession
# from random import choice

# from app import crud, schemas
# from .user import create_random_user

# from .utils import random_lower_string


# def get_random_todo_status():
#     return choice(["todo", "done", "in_progress"])


# def get_random_todo_priority():
#     return choice(["low", "medium", "high"])


# def create_random_todo(db: AsyncSession):
#     user = create_random_user(db)
#     title = random_lower_string()
#     content = random_lower_string()
#     status = get_random_todo_status()
#     priority = get_random_todo_priority()

#     todo_data = schemas.TodoCreate(
#         title=title,
#         content=content,
#         status=schemas.TodoStatus(status),
#         priority=schemas.TodoPriority(priority),
#     )

#     todo = crud.create_todo(db, todo=todo_data, user_id=user.id)

#     return todo
