# SPDX-FileCopyrightText: 2026 Filmhuis Den Haag
# SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends
from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession

from fhdhview.api.deps import get_session
from fhdhview.core.config import settings
from fhdhview.models.screening import Screening
from fhdhview.schemas.screening import ScreeningRead

router = APIRouter(prefix="/screenings", tags=["Screenings"])


@router.get(
    "",
    response_model=list[ScreeningRead],
    summary="Get upcoming screenings for the infodesk"
)
async def get_infodesk_screenings(
    session: AsyncSession = Depends(get_session)
) -> list[ScreeningRead]:
    now = datetime.now(tz=ZoneInfo(settings.timezone))
    today = now.date()

    query = (
        select(Screening)
        .where(Screening.start > now - timedelta(minutes=10))
        .where(Screening.start < today + timedelta(days=1))
        .order_by(col(Screening.start))
        .limit(8)
    )
    screenings = await session.exec(query)
    return [ScreeningRead.model_validate(s) for s in screenings.all()]


@router.get(
    "/prices",
    response_model=dict,
    summary="Get pricing information"
)
async def get_screening_prices() -> dict:
    return settings.prices
