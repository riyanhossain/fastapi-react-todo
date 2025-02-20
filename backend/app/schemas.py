from datetime import datetime
import enum
from typing import Optional
from pydantic import BaseModel, ConfigDict


class TodoStatus(enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TodoPriority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TodoBase(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    status: TodoStatus
    priority: TodoPriority
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    id: int
    name: str
    email: str
    password: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class TodoCreate(BaseModel):
    user_id: int
    title: str
    content: str
    status: TodoStatus
    priority: TodoPriority


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
