from datetime import timedelta
from fastapi import HTTPException, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models, schemas
from sqlalchemy.exc import IntegrityError
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
)


# Auth(Signup, Login)


async def sign_up(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(
        **user.model_dump(exclude={"password"}),
        password=get_password_hash(user.password)
    )
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
        return {
            "success": True,
            "data": {
                "id": db_user.id,
                "email": db_user.email,
                "name": db_user.name,
            },
            "message": "User created successfully",
        }
    except IntegrityError:
        await db.rollback()
        return HTTPException(
            status_code=400,
            detail={
                "success": False,
                "message": "User already exists",
            },
        )


async def login(response: Response, db: AsyncSession, user: schemas.UserLogin):
    result = await db.execute(
        select(models.User).where(models.User.email == user.email)
    )
    db_user = result.scalars().first()

    if not db_user:
        return HTTPException(
            status_code=404,
            detail={
                "success": False,
                "message": "User not found",
            },
        )

    if not verify_password(user.password, db_user.password):
        return HTTPException(
            status_code=400,
            detail={
                "success": False,
                "message": "Incorrect password",
            },
        )

    access_token = create_access_token(
        subject=db_user.email, expires_delta=timedelta(minutes=15)
    )
    refresh_token = create_refresh_token(
        subject=db_user.email, expires_delta=timedelta(days=7)
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=True,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        secure=True,
    )

    return {
        "success": True,
        "data": {
            "id": db_user.id,
            "email": db_user.email,
            "name": db_user.name,
        },
        "message": "Login successful",
    }



    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")

    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        new_access_token = create_access_token({"sub": email})

        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            samesite="Lax",
            secure=True,
        )

        return {"success": True, "message": "Token refreshed"}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


async def get_todos(db: AsyncSession):
    result = await db.execute(select(models.Todo))
    return result.scalars().all()


async def create_todo(db: AsyncSession, todo: schemas.TodoCreate):
    db_todo = models.Todo(**todo.model_dump())
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo


# async def get_users(db: AsyncSession):
#     result = await db.execute(select(models.User))
#     users = result.scalars().all()

#     return [
#         schemas.Userbase.model_validate(user, from_attributes=True)
#         for user in users
#     ]
