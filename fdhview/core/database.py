# SPDX-FileCopyrightText: 2026 Filmhuis Den Haag
# SPDX-License-Identifier:

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from fdhview.core.config import settings

sqlite_url = f"sqlite+aiosqlite:///{settings.sql_file_name}"

engine = create_async_engine(sqlite_url, echo=settings.debug)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
