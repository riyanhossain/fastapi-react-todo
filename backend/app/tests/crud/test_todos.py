import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.schemas import TodoCreate, TodoUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.todo import get_random_todo_priority, get_random_todo_status
from app.tests.utils.utils import random_lower_string
from app import schemas


@pytest.mark.asyncio
async def test_create_todo(db: AsyncSession):
    user_obj = await create_random_user(db)
    user = user_obj["data"]

    title = random_lower_string()
    content = random_lower_string()
    status = get_random_todo_status()
    priority = get_random_todo_priority()

    todo_in = TodoCreate(
        title=title,
        content=content,
        status=schemas.TodoStatus(status),
        priority=schemas.TodoPriority(priority),
    )

    todo = await crud.create_todo(db, todo_in, str(user["id"]))

    assert todo is not None
    assert todo["success"] is True
    assert todo["data"].title == title
    assert todo["data"].content == content
    assert todo["data"].status == status
    assert todo["data"].priority == priority


@pytest.mark.asyncio
async def test_update_todo(db: AsyncSession):
    user_obj = await create_random_user(db)
    user = user_obj["data"]

    # First create a todo
    title = random_lower_string()
    content = random_lower_string()
    status = get_random_todo_status()
    priority = get_random_todo_priority()

    todo_in = TodoCreate(
        title=title,
        content=content,
        status=schemas.TodoStatus(status),
        priority=schemas.TodoPriority(priority),
    )
    todo = await crud.create_todo(db, todo_in, str(user["id"]))

    # Now update it
    new_title = random_lower_string()
    new_status = get_random_todo_status()

    todo_update = TodoUpdate(title=new_title, status=schemas.TodoStatus(new_status))
    updated_todo = await crud.update_todo(db, todo=todo_update, todo_id=todo["data"].id)

    assert updated_todo["success"] is True
    assert updated_todo["data"].title == new_title
    assert updated_todo["data"].status == new_status
    assert updated_todo["data"].content == content


@pytest.mark.asyncio
async def test_delete_todo(db: AsyncSession):
    user_obj = await create_random_user(db)
    user = user_obj["data"]

    # First create a todo
    title = random_lower_string()
    content = random_lower_string()
    status = get_random_todo_status()
    priority = get_random_todo_priority()

    todo_in = TodoCreate(
        title=title,
        content=content,
        status=schemas.TodoStatus(status),
        priority=schemas.TodoPriority(priority),
    )
    todo = await crud.create_todo(db, todo_in, str(user["id"]))

    assert todo is not None

    # Now delete it
    delete_result = await crud.delete_todo(db, todo["data"].id)

    assert delete_result["success"] is True
    assert delete_result["message"] == "Todo deleted successfully"
