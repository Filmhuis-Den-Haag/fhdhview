# SPDX-FileCopyrightText: 2026 Filmhuis Den Haag
# SPDX-License-Identifier: AGPL-3.0-or-later

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    debug: bool = False
    api_password: str = "testertje"
    sql_file_name: str = "database.db"
    timezone: str = "Europe/Amsterdam"
    prices: dict = {
        "prijzen": [
            {"label": "Standaard", "price": "€ 12,50"},
            {"label": "Dagtarief (ma–vr tot 16u)", "price": "€ 11,00"},
            {"label": "Cineville", "price": "Gratis"},
            {"label": "Lange film (>180 min)", "price": "€ 15,00"},
            {"label": "70MM film", "price": "€ 15,00"},
        ],
        "kortingsprijzen": [
            {"label": "Jongeren (t/m 26 jaar)", "price": "€ 10,00"},
            {"label": "Student Nights", "price": "€ 5,00"},
            {"label": "CJP", "price": "€ 10,00"},
            {"label": "Vrienden", "price": "€ 9,50"},
            {"label": "Kinderfilm (t/m 11 jaar)", "price": "€ 8,00"},
            {"label": "Ooievaarspas", "price": "€ 6,25"},
            {"label": "De Volharding", "price": "€ 9,00"},
        ],
    }

settings = Settings()
