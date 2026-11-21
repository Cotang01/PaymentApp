from collections.abc import AsyncGenerator

import pytest_asyncio
from fastapi import FastAPI
from sqlalchemy import insert, select

from src.features.accounts.models import User
from src.features.accounts.router_user import router as user_router
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


async def test_create_user(test_client_factory: ClientFactory, test_app):
    async with test_client_factory(test_app) as client:
        response = await client.post(
            "/users", 
            json={"first_name": "John",
                  "second_name": "Doe", 
                  "email": "john@example.com", 
                  "password": "password"})
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "first_name": "John",
            "second_name": "Doe", 
            "email": "john@example.com"
            }


async def test_get_user_by_id(test_client_factory: ClientFactory, 
                              test_app,
                              test_async_sessionmaker):
    async with test_async_sessionmaker() as session:
        res = await session.execute(insert(User).values(
            first_name="John", 
            second_name="Doe", 
            email="john@example.com",
            hashed_password="password").returning(User.id))
        uid = res.scalar()
    async with test_client_factory(test_app) as client:
        response = await client.get(f"/users/{uid}")
        assert response.status_code == 200
        assert response.json() == {
            "id": uid, 
            "first_name": "John", 
            "second_name": "Doe", 
            "email": "john@example.com"
            }