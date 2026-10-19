# SPDX-FileCopyrightText: 2026 Filmhuis Den Haag
# SPDX-License-Identifier: AGPL-3.0-or-later

from sqlmodel import delete
from sqlmodel.ext.asyncio.session import AsyncSession

from fdhview.models.enums import Screen
from fdhview.models.screening import KijkWijzer, Screening
from fdhview.models.tags import kijkwijzer, screens
from fdhview.services.screenwriter.schema import AAMPos

# Delimiters used to attach notes to titles
DASH_DELIMITERS = (" - ", " – ", " — ", "- ")

# Explicit list of known screening notes (exact matches only)
KNOWN_SCREENING_NOTES = frozenset({
    # Subtitles
    "en subs",
    "en sub",
    "nl subs",
    "nl sub",

    # Events & talks
    "met inleiding",
    "met nagesprek",
    "met inleiding en nagesprek",
    "met voorfilms en nagesprek",

    # Combined notes
    "en subs met inleiding",
    "en subs en nagesprek",
})


def _clean_title(title: str) -> str:
    """Peel off trailing presentation notes using an explicit blacklist."""
    for dash in DASH_DELIMITERS:
        while dash in title:
            prefix, _, suffix = title.rpartition(dash)
            # Exact string check (case-insensitive and trimmed)
            if suffix.strip().lower() in KNOWN_SCREENING_NOTES:
                title = prefix.strip()
            else:
                break

    return title.strip()


async def import_sessions(data: AAMPos, session: AsyncSession):
    # purge old rows
    await session.exec(delete(Screening))

    # add new screenings from data
    for screening in data.sessions.root:

        kijk: list[KijkWijzer] = []
        for k in kijkwijzer:
            if k in screening.attributes:
                kijk.append(kijkwijzer[k])
                screening.attributes.remove(k)

        if "EN subs" in screening.attributes:
            en_subs = True
            screening.attributes.remove("EN subs")
        else:
            en_subs = False

        if "with introduction" in screening.attributes:
            intro = True
            screening.attributes.remove("with introduction")
        else:
            intro = False

        if "with after talk" in screening.attributes:
            outro = True
            screening.attributes.remove("with after talk")
        else:
            outro = False

        new_screening = Screening(
            session=screening.session_id,
            screen=screens.get(screening.screen_identifier, Screen.ONE),
            complex_ident=screening.complex_identifier,
            start=screening.start,
            end=screening.end,
            duration=screening.feature_duration,
            title=_clean_title(screening.title),
            rating=screening.rating,
            seats_total=screening.seats_available,
            seats_sold=screening.seats_sold,
            en_subs=en_subs,
            intro=intro,
            outro=outro,
            kijkwijzer=kijk,
            tags=screening.attributes
        )

        session.add(new_screening)
    await session.commit()
