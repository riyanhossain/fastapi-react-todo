from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from app.tests.utils.utils import get_token_headers
from app.tests.utils.todo import (
    create_random_todo,
    get_random_todo_status,
    get_random_todo_priority,
)
from app.core.config import settings
from app.tests.utils.user import create_random_user


@pytest.mark.asyncio
async def test_create_todo(client: TestClient, db: AsyncSession):
    user = await create_random_user(db)

    test_todo = {
        "title": "Test Todo",
        "content": "Test Content",
        "status": "todo",
        "priority": "low",
    }

    headers = get_token_headers(user["data"]["email"])

    response = client.post(
        f"{settings.API_V1_STR}/todos/create", json=test_todo, headers=headers
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["title"] == test_todo["title"]
    assert response.json()["message"] == "Todo created successfully"


@pytest.mark.asyncio
async def test_update_todo(client: TestClient, db: AsyncSession):
    # Create a user and a todo
    todo_data = await create_random_todo(db)
    user = todo_data["user"]
    todo = todo_data["todo"]["data"]

    # Print todo type to debug
    print(f"Todo type: {type(todo)}")
    print(f"Todo dir: {dir(todo)}")

    # Prepare update data
    update_data = {
        "title": "Updated Todo Title",
        "status": get_random_todo_status(),
        "priority": get_random_todo_priority(),
    }

    headers = get_token_headers(user["data"]["email"])

    # Update the todo - use attribute access for Todo object
    response = client.patch(
        f"{settings.API_V1_STR}/todos/update/{todo.id}",
        json=update_data,
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["title"] == update_data["title"]
    assert response.json()["message"] == "Todo updated successfully"


@pytest.mark.asyncio
async def test_delete_todo(client: TestClient, db: AsyncSession):
    # Create a user and a todo
    todo_data = await create_random_todo(db)
    user = todo_data["user"]
    todo = todo_data["todo"]["data"]

    # Print todo type to debug
    print(f"Todo type: {type(todo)}")
    print(f"Todo dir: {dir(todo)}")

    headers = get_token_headers(user["data"]["email"])

    # Delete the todo - use attribute access for Todo object
    response = client.delete(
        f"{settings.API_V1_STR}/todos/delete/{todo.id}", headers=headers
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["message"] == "Todo deleted successfully"


@pytest.mark.asyncio
async def test_create_todo_unauthorized(client: TestClient):
    # Try to create a todo without authentication
    test_todo = {
        "title": "Test Todo",
        "content": "Test Content",
        "status": "todo",
        "priority": "low",
    }

    response = client.post(f"{settings.API_V1_STR}/todos/create", json=test_todo)

    assert response.status_code == 401
