from collections.abc import AsyncGenerator

import pytest_asyncio
from fastapi import FastAPI

from src.features.user.router import router as user_router
from tests.conftest import ClientFactory


@pytest_asyncio.fixture
async def test_app() -> AsyncGenerator[FastAPI]:
    app = FastAPI()
    app.include_router(user_router)
    yield app


async def test_get_users_on_empty_db(test_client_factory: ClientFactory, test_app):
    async with test_client_factory(test_app) as client:
        response = await client.get("/users")
        assert response.status_code == 200
        assert response.json() == []
        