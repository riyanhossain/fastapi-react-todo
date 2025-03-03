from datetime import datetime, timedelta, timezone
from typing import Any
from fastapi import Depends, HTTPException, Request, Response
from passlib.context import CryptContext
from app.core import database
from app.core.config import settings
import jwt
from app import crud


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    #print(f"Token Expiry (UTC): {expire}")
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.REFRESH_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(request: Request, db=Depends(database.get_db)):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=401, detail={"success": False, "message": "Not authenticated"}
        )

    try:
        #print(f"Token received: {token}")  # Debugging
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])

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


async def refresh_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(
            status_code=401, detail={"success": False, "message": "No refresh token"}
        )

    try:
        payload = jwt.decode(
            refresh_token, settings.REFRESH_KEY, algorithms=[ALGORITHM]
        )

        email: str = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code=401,
                detail={"success": False, "message": "Invalid refresh token"},
            )

        new_access_token = create_access_token(
            subject=email, expires_delta=timedelta(minutes=15)
        )

        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            samesite="lax",
            secure=True,
        )

        return {"success": True, "message": "Token refreshed"}

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401, detail={"success": False, "message": "Token has expired"}
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401, detail={"success": False, "message": "Invalid token"}
        )


# Auth(Middleware)


