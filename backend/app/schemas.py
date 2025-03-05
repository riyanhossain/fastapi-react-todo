from datetime import datetime
from enum import Enum
from typing import Optional, TypedDict
from pydantic import UUID4, BaseModel


class TodoStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TodoPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TodoBase(BaseModel):
    id: UUID4
    user_id: int
    title: str
    content: str
    status: TodoStatus
    priority: TodoPriority
    created_at: datetime
    updated_at: datetime


class TodoCreate(BaseModel):
    user_id: Optional[UUID4] = None
    title: str
    content: str
    status: TodoStatus
    priority: TodoPriority


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    status: Optional[TodoStatus] = None
    priority: Optional[TodoPriority] = None


class UserBase(BaseModel):
    id: UUID4
    name: str
    email: str
    password: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None


# Define response schema using TypedDict
class UserData(TypedDict):
    id: int
    email: str
    name: str


class SuccessResponse(TypedDict):
    success: bool
    data: UserData
    message: str


class ErrorResponse(TypedDict):
    success: bool
    message: str
