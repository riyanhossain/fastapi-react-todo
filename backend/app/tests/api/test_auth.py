import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.tests.utils.utils import random_email, random_lower_string


@pytest.mark.asyncio
async def test_signup(client: TestClient):
    name = random_lower_string()
    email = random_email()
    password = random_lower_string()

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


@pytest.mark.asyncio
async def test_login(client: TestClient):
    # First create a user
    name = random_lower_string()
    email = random_email()
    password = random_lower_string()

    client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json={
            "name": name,
            "email": email,
            "password": password,
        },
    )

    # Now try to login
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["email"] == email
    assert "access_token" in response.cookies


@pytest.mark.asyncio
async def test_login_wrong_password(client: TestClient):
    # First create a user
    name = random_lower_string()
    email = random_email()
    password = random_lower_string()

    client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json={
            "name": name,
            "email": email,
            "password": password,
        },
    )

    # Try to login with wrong password
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        json={
            "email": email,
            "password": "wrong_password",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"]["success"] is False
    assert "access_token" not in response.cookies
