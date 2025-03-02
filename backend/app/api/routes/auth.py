from fastapi import APIRouter, Depends
from app.core import database
from app import crud, schemas


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
async def signup(user: schemas.UserCreate, db=Depends(database.get_db)):
    return await crud.sign_up(db, user)


@router.post("/login", response_model=schemas.UserResponse)
async def login(user: schemas.UserResponse, db=Depends(database.get_db)):
    return await crud.get_users(db)
