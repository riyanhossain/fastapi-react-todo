from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models, schemas
from sqlalchemy.exc import IntegrityError


# Auth


async def sign_up(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except IntegrityError:
        await db.rollback()
        return HTTPException(status_code=400, detail="User already exists")

# async def login(db: AsyncSession, user: schemas.UserResponse):
#     result = await db.execute(select(models.User).where(models.User.email == user.email))
#     db_user = result.scalars().first()
#     if db_user is None:
#         return HTTPException(status_code=400, detail="User not found")
#     if db_user.password != user.password:
#         return HTTPException(status_code=400, detail="Incorrect password")
#     return db_user




async def get_todos(db: AsyncSession):
    result = await db.execute(select(models.Todo))
    return result.scalars().all()


async def create_todo(db: AsyncSession, todo: schemas.TodoCreate):
    db_todo = models.Todo(**todo.model_dump())
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo


async def get_users(db: AsyncSession):
    result = await db.execute(select(models.User))
    users = result.scalars().all()

    return [
        schemas.UserResponse.model_validate(user, from_attributes=True)
        for user in users
    ]
