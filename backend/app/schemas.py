from datetime import datetime
import enum
from pydantic import BaseModel


class TodoStatus(enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TodoPriority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TodoCreate(BaseModel):
    user: int
    title: str
    content: str
    status: TodoStatus
    priority: TodoPriority


class TodoBase(BaseModel):
    id: int
    user: int
    title: str
    content: str
    status: TodoStatus
    priority: TodoPriority
    created_at: datetime
    updated_at: datetime


class UserBase(BaseModel):
    id: int
    name: str
    email: str
    password: str
    created_at: datetime
    updated_at: datetime


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
