from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import database
from app import crud, schemas

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/", response_model=list[schemas.TodoBase])
async def read_todos(db: AsyncSession = Depends(database.get_db)):
    return await crud.get_todos(db)


@router.post("/", response_model=schemas.TodoCreate)
async def create_todo(
    todo: schemas.TodoCreate, db: AsyncSession = Depends(database.get_db)
):
    return await crud.create_todo(db, todo)
