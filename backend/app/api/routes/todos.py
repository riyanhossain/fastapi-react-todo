from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import database
from app import crud, schemas
from app.core import security

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("/create")
async def create_todo(
    todo: schemas.TodoCreate,
    db: AsyncSession = Depends(database.get_db),
    user: schemas.UserBase = Depends(security.get_current_user),
):
    return await crud.create_todo(db, todo, user)
