import os
from collections.abc import AsyncGenerator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager

import pytest_asyncio
from dotenv import load_dotenv
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert, select
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.database import Base
from src.core.dependencies import get_db
from src.features.accounts.models import User

ClientFactory = Callable[[FastAPI], AbstractAsyncContextManager[AsyncClient]]

load_dotenv()


@pytest_asyncio.fixture(scope="session")
async def test_async_engine():
    db_url = URL.create(
    drivername="postgresql+asyncpg", 
    username=os.getenv("POSTGRES_USER", "dev_user"),
    password=os.getenv("POSTGRES_PASSWORD", "dev_password"),
    host="localhost",
    port=int(os.getenv("POSTGRES_PORT", "5432")),
    database=os.getenv("TEST_POSTGRES_DB", "test_db")
    )
    engine = create_async_engine(url=db_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
            
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        
    await engine.dispose()



@pytest_asyncio.fixture
async def test_async_sessionmaker(
    test_async_engine: AsyncEngine
    ) -> AsyncGenerator[async_sessionmaker[AsyncSession]]:
    connection = await test_async_engine.connect()
    transaction = await connection.begin()
    try:
        yield async_sessionmaker(bind=connection, expire_on_commit=False)
    finally:
        await transaction.rollback()
        await connection.close()
    


@pytest_asyncio.fixture
async def test_client_factory(test_async_sessionmaker) -> ClientFactory:
    
    @asynccontextmanager
    async def _create_client(app: FastAPI) -> AsyncGenerator[AsyncClient]:
        
        async def overrides_get_db() -> AsyncGenerator[AsyncSession]:
            async with test_async_sessionmaker() as session:
                yield session
        
        client = AsyncClient(transport=ASGITransport(app=app), 
                             base_url="http://test")
        app.dependency_overrides[get_db] = overrides_get_db
        try:
            yield client
        finally:
            app.dependency_overrides.clear()
            await client.aclose()
    
    return _create_client


@pytest_asyncio.fixture
async def create_user(test_async_sessionmaker: async_sessionmaker[AsyncSession]):
    # TODO create user creation factory fixture
    async def _create(user_data: dict[str, str]) -> User:
        async with test_async_sessionmaker() as session:
            pass
    
    return _create
