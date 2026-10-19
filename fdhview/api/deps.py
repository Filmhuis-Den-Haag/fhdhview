# SPDX-FileCopyrightText: 2026 Filmhuis Den Haag
# SPDX-License-Identifier: AGPL-3.0-or-later

import secrets
from collections.abc import AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlmodel.ext.asyncio.session import AsyncSession

from fdhview.core.config import settings
from fdhview.core.database import async_session

security = HTTPBasic()


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session


def check_auth(credentials: HTTPBasicCredentials = Depends(security)):
    if not secrets.compare_digest(credentials.password.encode(), settings.api_password.encode()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
