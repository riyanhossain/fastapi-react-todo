from fastapi import APIRouter
from app import crud, schemas
from app.api.deps import CurrentUser, SessionDep


router = APIRouter(prefix="/users", tags=["users"])


@router.patch("/update/{user_id}")
async def update_user(
    user_data: schemas.UserUpdate,
    user_id: str,
    db: SessionDep,
    user: CurrentUser,
):
    return await crud.update_user(db, user_id, user_data)
