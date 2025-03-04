from typing import Annotated
from fastapi import Depends, HTTPException, Request
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import database
from app.core.config import settings
from app import crud
from app.models import User


SessionDep = Annotated[AsyncSession, Depends(database.get_db)]


async def get_current_user(request: Request, db: SessionDep) -> User:
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=401, detail={"success": False, "message": "Not authenticated"}
        )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        email: str = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code=401,
                detail={"success": False, "message": "Invalid token (email)"},
            )

        db_user = await crud.get_user_by_email(db, email)

        if db_user is None:
            raise HTTPException(
                status_code=404,
                detail={"success": False, "message": "User not found"},
            )

        return db_user

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401, detail={"success": False, "message": "Token has expired"}
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401, detail={"success": False, "message": "Invalid token"}
        )


CurrentUser = Annotated[User, Depends(get_current_user)]
