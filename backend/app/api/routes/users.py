from fastapi import APIRouter, Depends
from app.core import database
from app import crud, schemas


router = APIRouter(prefix="/users", tags=["users"])


@router.patch("/update/{user_id}")
async def update_user(
    user: schemas.UserUpdate,
    user_id: str,
    db=Depends(database.get_db),
):
    return await crud.update_user(db, user_id, user)
