from fastapi import APIRouter, Depends, Request, Response
from app.core import database
from app import crud, schemas
from app.core import security


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
async def signup(user: schemas.UserCreate, db=Depends(database.get_db)):
    return await crud.create_user(db, user)


@router.post("/login")
async def login(
    response: Response, user: schemas.UserLogin, db=Depends(database.get_db)
):
    return await crud.login(response, db, user)


@router.post("/refresh-token")
async def refresh_token(request: Request, response: Response):
    return await security.refresh_token(request, response)
