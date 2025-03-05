import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.schemas import UserCreate
from app.tests.utils.utils import random_email, random_lower_string


@pytest.mark.asyncio
async def test_create_user(db: AsyncSession):
    email = random_email()
    password = random_lower_string()
    name = random_lower_string()
    user_in = UserCreate(email=email, password=password, name=name)

    r = await crud.create_user(db, user_in)

    assert r["success"] is True
    assert r["data"]["email"] == email
    assert r["data"]["name"] == name
    assert "id" in r["data"]


@pytest.mark.asyncio
async def test_get_user_by_email(db: AsyncSession):
    email = random_email()
    password = random_lower_string()
    name = random_lower_string()
    user_in = UserCreate(email=email, password=password, name=name)

    user = await crud.create_user(db, user_in)
    user_by_email = await crud.get_user_by_email(db, email)

    assert user_by_email
    assert user["data"]["email"] == user_by_email.email
    assert user["data"]["name"] == user_by_email.name
    assert user["data"]["id"] == user_by_email.id
