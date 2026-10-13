from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends
from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession

from fdhview.api.deps import get_session
from fdhview.core.config import settings
from fdhview.models.screening import Screening
from fdhview.schemas.screening import ScreeningRead

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

    query = (
        select(Screening)
        .where(Screening.start > now)
        .order_by(col(Screening.start))
        .limit(7)
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
