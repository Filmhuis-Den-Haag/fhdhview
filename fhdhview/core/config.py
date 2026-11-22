# SPDX-FileCopyrightText: 2026 Filmhuis Den Haag
# SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import date

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PriceRow(BaseModel):
    label: str
    price: str
    price_new: str | None = None

class PriceTable(BaseModel):
    prijzen: list[PriceRow] = Field(min_length=1)
    kortingsprijzen: list[PriceRow] = []
    price_start: date | None = None


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    debug: bool = False
    api_password: str = "testertje"
    sql_file_name: str = "database.db"
    timezone: str = "Europe/Amsterdam"
    prices: PriceTable = Field(default_factory=lambda: PriceTable(
        prijzen=[
            PriceRow(label="Standaard", price="€ 12,50", price_new="€ 13,00"),
            PriceRow(label="Dagtarief (ma–vr tot 16u)", price="€ 11,00", price_new="€ 11,50"),
            PriceRow(label="Cineville", price="Gratis", price_new="Gratis"),
            PriceRow(label="Lange film (>180 min)", price="€ 15,00", price_new="€ 15,50"),
            PriceRow(label="70MM film", price="€ 15,00", price_new="€ 15,50"),
        ],
        kortingsprijzen=[
            PriceRow(label="Jongeren (t/m 26 jaar)", price="€ 10,00"),
            PriceRow(label="Student Nights", price="€ 5,00"),
            PriceRow(label="CJP", price="€ 10,00"),
            PriceRow(label="Vrienden", price="€ 9,50"),
            PriceRow(label="Kinderfilm (t/m 11 jaar)", price="€ 8,00"),
            PriceRow(label="Ooievaarspas", price="€ 6,25"),
            PriceRow(label="De Volharding", price="€ 9,00"),
        ],
        price_start=date(2026, 12, 1)
    ))

settings = Settings()
