import asyncio
from collections.abc import AsyncGenerator, Iterator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from fdhview.api.deps import get_session
from fdhview.main import app

test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
test_session_maker = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(autouse=True)
def setup_test_db() -> Iterator[None]:
    """Creates tables before each test and drops them after."""
    async def _setup():
        async with test_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def _teardown():
        async with test_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)

    asyncio.run(_setup())
    yield
    asyncio.run(_teardown())


@pytest.fixture
def client() -> Iterator[TestClient]:
    """Test client that uses the in-memory database."""
    async def override_get_session():
        async with test_session_maker() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession]:
    """Async session for tests that need to seed or query data directly."""
    async with test_session_maker() as session:
        yield session
