from datetime import timedelta
from fastapi import HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import schemas, models
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
)


# Auth(Login)


async def login(response: Response, db: AsyncSession, user: schemas.UserLogin):
    result = await db.execute(
        select(models.User).where(models.User.email == user.email)
    )
    db_user = result.scalars().first()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "message": "User not found",
            },
        )

    if not verify_password(user.password, db_user.password):
        raise HTTPException(
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


# Todo(Create, Update, Delete, Get)


async def create_todo(
    db: AsyncSession, todo: schemas.TodoCreate, user: schemas.UserBase
):
    db_todo = models.Todo(**todo.model_dump(exclude={"user_id"}), user_id=user.id)
    db.add(db_todo)
    try:
        await db.commit()
        await db.refresh(db_todo)
        return {
            "success": True,
            "data": db_todo,
            "message": "Todo created successfully",
        }
    except HTTPException:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "message": "Todo creation failed",
            },
        )


async def update_todo(db: AsyncSession, todo: schemas.TodoUpdate, todo_id: str):
    result = await db.execute(select(models.Todo).where(models.Todo.id == todo_id))
    db_todo = result.scalars().first()

    if not db_todo:
        raise HTTPException(
            status_code=404, detail={"success": False, "message": "Todo not found"}
        )

    update_data = todo.model_dump(exclude={"id", "user_id"})

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail={"success": False, "message": "No valid fields to update"},
        )

    try:
        for key, value in update_data.items():
            setattr(db_todo, key, value)

        await db.commit()
        await db.refresh(db_todo)

        return {
            "success": True,
            "data": db_todo,
            "message": "Todo updated successfully",
        }

    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail={"success": False, "message": "Database error occurred"},
        )


async def delete_todo(db: AsyncSession, todo_id: str):
    result = await db.execute(select(models.Todo).where(models.Todo.id == todo_id))
    db_todo = result.scalars().first()

    if not db_todo:
        raise HTTPException(
            status_code=404, detail={"success": False, "message": "Todo not found"}
        )

    try:
        await db.delete(db_todo)
        await db.commit()
        return {
            "success": True,
            "message": "Todo deleted successfully",
        }
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail={"success": False, "message": "Database error occurred"},
        )


# User (Get, Update, Delete)


async def create_user(db: AsyncSession, user: schemas.UserCreate):
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
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "message": "User already exists",
            },
        )


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).where(models.User.email == email))
    return result.scalars().first()


async def update_user(db: AsyncSession, user_id: str, user_data: schemas.UserUpdate):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    db_user = result.scalars().first()

    if not db_user:
        raise HTTPException(
            status_code=404, detail={"success": False, "message": "User not found"}
        )

    update_data = user_data.model_dump(
        exclude={"id", "created_at", "updated_at", "password", "email"}
    )

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail={"success": False, "message": "No valid fields to update"},
        )

    try:
        for key, value in update_data.items():
            setattr(db_user, key, value)

        await db.commit()
        await db.refresh(db_user)

        return {
            "success": True,
            "data": db_user,
            "message": "User updated successfully",
        }

    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail={"success": False, "message": "Database error occurred"},
        )
