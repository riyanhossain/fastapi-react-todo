from fastapi import APIRouter, Depends
from app.core import database
from app import crud, schemas


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def read_users(db=Depends(database.get_db)):
    return await crud.get_users(db)


@router.post("/")
async def create_user(user: schemas.UserCreate, db=Depends(database.get_db)):
    return await crud.create_user(db, user)
