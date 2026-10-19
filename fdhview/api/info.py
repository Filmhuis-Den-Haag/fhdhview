# SPDX-FileCopyrightText: 2026 Filmhuis Den Haag
# SPDX-License-Identifier:

from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

BASE_DIR = Path(__file__).resolve().parent.parent

router = APIRouter(
    prefix="/info",
    tags=["Info"]
)


@router.get("", response_class=FileResponse)
async def get_info():
    return FileResponse(BASE_DIR / "html" / "info.html")
