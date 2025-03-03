from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import database
from app import crud, schemas
from app.api.deps import get_current_user
from app import models

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("/create")
async def create_todo(
    todo: schemas.TodoCreate,
    db: AsyncSession = Depends(database.get_db),
    user: schemas.UserBase = Depends(get_current_user),
):
    return await crud.create_todo(db, todo, user)


@router.patch("/update/{todo_id}")
async def update_todo(
    todo: schemas.TodoUpdate,
    todo_id: str,
    db: AsyncSession = Depends(database.get_db),
    user: schemas.UserBase = Depends(get_current_user),
):
    return await crud.update_todo(db, todo, todo_id)


@router.delete("/delete/{todo_id}")
async def delete_todo(
    todo_id: str,
    db: AsyncSession = Depends(database.get_db),
    user: schemas.UserBase = Depends(get_current_user),
):
    return await crud.delete_todo(db, todo_id)
