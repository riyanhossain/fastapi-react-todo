from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.schemas import UserCreate
from app.tests.utils.utils import random_email, random_lower_string


def create_random_user(db: AsyncSession):
    email = random_email()
    password = random_lower_string()
    name = random_lower_string()

    user = crud.create_user(db, UserCreate(name=name, email=email, password=password))
    return user    
