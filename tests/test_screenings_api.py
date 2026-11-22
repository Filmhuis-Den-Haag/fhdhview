# SPDX-FileCopyrightText: 2026 Filmhuis Den Haag
# SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from fhdhview.core.config import settings
from fhdhview.models.enums import Screen
from fhdhview.models.screening import Screening


@pytest.mark.asyncio
async def test_infodesk_filters_past(
    client, db_session: AsyncSession
):
    now = datetime.now(tz=ZoneInfo(settings.timezone))

    # Past film (ended 15 mins ago)
    past = Screening(
        session=1, screen=Screen.ONE, complex_ident="FDH",
        start=now - timedelta(hours=2), end=now - timedelta(minutes=15),
        duration=105, title="Past Film", rating=0, seats_total=100, seats_sold=10
    )
    # Currently running film (started 30 mins ago, ends in 60 mins)
    running = Screening(
        session=2, screen=Screen.TWO, complex_ident="FDH",
        start=now - timedelta(minutes=30), end=now + timedelta(minutes=60),
        duration=90, title="Running Film", rating=0, seats_total=100, seats_sold=50
    )
    # Upcoming film (starts in 2 hours)
    upcoming = Screening(
        session=3, screen=Screen.THREE, complex_ident="FDH",
        start=now + timedelta(hours=2), end=now + timedelta(hours=4),
        duration=120, title="Upcoming Film", rating=0, seats_total=100, seats_sold=20
    )

    db_session.add_all([past, running, upcoming])
    await db_session.commit()

    response = client.get("/api/screenings")
    assert response.status_code == 200

    titles = [s["title"] for s in response.json()]
    assert "Past Film" not in titles
    assert "Running Film" not in titles
    assert "Upcoming Film" in titles


@pytest.mark.asyncio
async def test_get_screening_prices(client):
    response = client.get("/api/screenings/prices")
    assert response.status_code == 200
    assert response.json() == settings.prices.model_dump(mode="json")
