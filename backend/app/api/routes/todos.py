from fastapi import APIRouter, Depends
from app import crud, schemas
from app.api.deps import CurrentUser, SessionDep

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("/create")
async def create_todo(
    todo: schemas.TodoCreate,
    db: SessionDep,
    user: CurrentUser,
):
    return await crud.create_todo(db, todo, user)


@router.patch("/update/{todo_id}")
async def update_todo(
    todo: schemas.TodoUpdate,
    todo_id: str,
    db: SessionDep,
    user: CurrentUser,
):
    return await crud.update_todo(db, todo, todo_id)


@router.delete("/delete/{todo_id}")
async def delete_todo(
    todo_id: str,
    db: SessionDep,
    user: CurrentUser,
):
    return await crud.delete_todo(db, todo_id)
