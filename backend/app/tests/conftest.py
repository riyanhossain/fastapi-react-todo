from typing import Generator, AsyncGenerator
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.main import app
from app.core.database import Base, get_db


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_DATABASE_URL, echo=True)

TestingSessionLocal = async_sessionmaker(
    bind=engine, expire_on_commit=False, autoflush=False
)


@pytest_asyncio.fixture(scope="function")
async def db() -> AsyncGenerator[AsyncSession, None]:
    """
    Create a fresh database on each test case.
    """
    # Create the tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create a session for testing
    async with TestingSessionLocal() as session:
        yield session

    # Drop the tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
def client(db: AsyncSession) -> Generator[TestClient, None, None]:
    """
    Create a test client that uses the test database.
    """

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
