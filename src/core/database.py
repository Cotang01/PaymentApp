from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from src.app.config import settings

DB_URL = URL.create(
    drivername="postgresql+asyncpg", 
    username=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    host=settings.POSTGRES_HOST,
    port=settings.POSTGRES_PORT,
    database=settings.POSTGRES_DB
    )

engine = create_async_engine(url=DB_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=engine)

Base = declarative_base()
