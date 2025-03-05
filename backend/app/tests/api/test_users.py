import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.tests.utils.utils import get_token_headers, random_email, random_lower_string


@pytest.mark.asyncio
async def test_update_user(client: TestClient):
    name = random_lower_string()
    email = random_email()
    password = random_lower_string()

    # First create a user
    response = client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json={
            "name": name,
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["email"] == email
    assert "id" in response.json()["data"]
    assert "password" not in response.json()["data"]

    # Now try to update the user name
    new_name = random_lower_string()

    user = response.json()["data"]

    response = client.patch(
        f"{settings.API_V1_STR}/users/update/{user['id']}",
        json={
            "name": new_name,
        },
        headers=get_token_headers(email),
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["name"] == new_name
    assert "email" not in response.json()["data"]
    assert "id" not in response.json()["data"]
    assert "password" not in response.json()["data"]
