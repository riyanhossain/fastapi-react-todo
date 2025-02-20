from sqlalchemy import Column, DateTime, Enum, Integer, String, ForeignKey, func
from app.database import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(
        Integer, primary_key=True, index=True, nullable=False, autoincrement=True
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    title = Column(String, index=True, nullable=False)
    content = Column(String, nullable=False)
    status = Column(
        Enum("todo", "in_progress", "completed"), default="todo", nullable=False
    )
    priority = Column(Enum("low", "medium", "high"), default="low", nullable=False)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationship: Many Todos → One User
    # owner = relationship("User", back_populates="todos")


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer, primary_key=True, index=True, nullable=False, autoincrement=True
    )
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    # todos = relationship("Todo", back_populates="owner", cascade="all, delete-orphan")

    created_at = Column(
        DateTime(timezone=True),
        default=func.now(),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
