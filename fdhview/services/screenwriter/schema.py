# SPDX-FileCopyrightText: 2026 Filmhuis Den Haag
# SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime
from typing import Annotated
from zoneinfo import ZoneInfo

from pydantic import BeforeValidator
from pydantic_xml import BaseXmlModel, RootXmlModel, element, wrapped

from fdhview.core.config import settings

DT = Annotated[datetime, BeforeValidator(lambda v: datetime.strptime(v, "%Y%m%d%H%M").replace(
    tzinfo=ZoneInfo(settings.timezone)
))]


class Session(BaseXmlModel, tag='session'):
    session_id: int = element(tag='id')
    screen_identifier: str = element()
    complex_identifier: str = element()
    start: DT = element()
    end: DT = element()
    feature_duration: int = element()
    title: str = element()
    rating: int = element()
    seats_available: int = element()
    seats_sold: int = element()
    attributes: list[str] = wrapped('session_attributes', element(tag='session_attribute'))


class Sessions(RootXmlModel, tag='sessions'):
    root: list[Session]


class AAMPos(BaseXmlModel, tag='AAMPos'):
    sessions: Sessions = element()
