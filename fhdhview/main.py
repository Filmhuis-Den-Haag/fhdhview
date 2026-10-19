# SPDX-FileCopyrightText: 2026 Filmhuis Den Haag
# SPDX-License-Identifier: AGPL-3.0-or-later

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from fhdhview.api.admin import router as admin_router
from fhdhview.api.health import router as health_router
from fhdhview.api.info import router as info_router
from fhdhview.api.screenings import router as screenings_router
from fhdhview.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Runs on startup: ensure DB tables exist"""
    await init_db()
    yield


app = FastAPI(title="Filmhuis Den Haag Signage", lifespan=lifespan)

BASE_DIR = Path(__file__).resolve().parent

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

app.include_router(admin_router)
app.include_router(health_router)
app.include_router(info_router)
app.include_router(screenings_router, prefix="/api")
