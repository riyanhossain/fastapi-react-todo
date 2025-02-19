from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models, schemas


async def get_todos(db: AsyncSession):
    result = await db.execute(select(models.Todo))
    return result.scalars().all()


async def create_todo(db: AsyncSession, todo: schemas.TodoCreate):
    db_todo = models.Todo(**todo.dict())
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo


async def get_users(db: AsyncSession):
    result = await db.execute(select(models.User))
    return result.scalars().all()


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
