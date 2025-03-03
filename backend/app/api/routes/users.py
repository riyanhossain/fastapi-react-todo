from fastapi import APIRouter, Depends
from app.core import database
from app import crud, schemas
from app.api.deps import get_current_user


router = APIRouter(prefix="/users", tags=["users"])


@router.patch("/update/{user_id}")
async def update_user(
    user_data: schemas.UserUpdate,
    user_id: str,
    db=Depends(database.get_db),
    user: schemas.UserBase = Depends(get_current_user),
):
    return await crud.update_user(db, user_id, user_data)
