# SPDX-FileCopyrightText: 2026 Filmhuis Den Haag
# SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime

import sqlalchemy as sa
from pydantic import field_serializer, field_validator
from sqlmodel import Field, SQLModel

from fhdhview.models.enums import KijkWijzer, Screen


class Screening(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    session: int
    screen: Screen = Field(default=Screen.ONE, sa_column=sa.Column(sa.Enum(Screen)))
    complex_ident: str
    start: datetime
    end: datetime
    duration: int
    title: str
    rating: int
    seats_total: int
    seats_sold: int
    en_subs: bool = False
    intro: bool = False
    outro: bool = False
    kijkwijzer: list[KijkWijzer] = Field(default_factory=list, sa_type=sa.JSON)
    tags: list[str] = Field(default_factory=list, sa_type=sa.JSON)

    @field_validator("kijkwijzer", mode="before")
    @classmethod
    def _coerce(cls, v):
        return [r.value if isinstance(r, KijkWijzer) else r for r in v]

    @field_serializer("kijkwijzer")
    def _serialize(self, v: list[KijkWijzer]) -> list[str]:
        return [r.value if isinstance(r, KijkWijzer) else r for r in v]
