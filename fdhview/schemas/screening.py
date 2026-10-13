from datetime import datetime

from sqlmodel import SQLModel

from fdhview.models.enums import KijkWijzer, Screen


class ScreeningRead(SQLModel):
    screen: Screen
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
    kijkwijzer: list[KijkWijzer] = []
    tags: list[str] = []
