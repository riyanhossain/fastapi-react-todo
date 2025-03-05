from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.schemas import UserCreate
from app.tests.utils.utils import random_email, random_lower_string


async def create_random_user(db: AsyncSession):
    email = random_email()
    password = random_lower_string()
    name = random_lower_string()

    user_in = UserCreate(name=name, email=email, password=password)
    user = await crud.create_user(db, user_in)
    return {
        "data": user["data"] if isinstance(user, dict) else user,
        "email": email,
        "password": password,
    }
