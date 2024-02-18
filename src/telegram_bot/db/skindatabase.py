import os
from contextlib import asynccontextmanager
from typing import AsyncContextManager

from sqlalchemy import URL, MetaData

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    pass


class SkinDatabase:
    def __init__(self, url: str | URL):
        self._ulr = url
        self._engine = create_async_engine(url, echo=True, pool_pre_ping=True)

    async def proceed_schemas(self, metadata: MetaData) -> None:
        async with self._engine.begin() as connection:
            await connection.run_sync(metadata.create_all)

    async def drop_all_tables(self, metadata: MetaData) -> None:
        async with self._engine.begin() as connection:
            await connection.run_sync(metadata.drop_all)

    def get_session_maker(self) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            self._engine, expire_on_commit=False, autocommit=False
        )