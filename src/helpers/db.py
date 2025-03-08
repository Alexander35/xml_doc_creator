from typing import AsyncGenerator
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from config import settings
from enum import Enum as PyEnum

engine = create_async_engine(settings.postgres_url)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

class EntityIdType(PyEnum):
    ace = 'ace'
    lei = 'lei'
    bic = 'bic'
    eic = 'eic'
    gln = 'gln'

class TradingCapacityType(PyEnum):
    P = 'P'
    A = 'A'

class BuySellIndicatorType(PyEnum):
    B = 'B'
    S = 'S'
    C = 'C'
