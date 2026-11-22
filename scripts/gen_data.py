from datetime import datetime, timedelta
from random import randint, sample
from zoneinfo import ZoneInfo

from faker import Faker
from faker.providers import company

from fhdhview.services.screenwriter.schema import AAMPos, Session, Sessions

fake = Faker()
fake.add_provider(company)

zaal = [
    "DenHaag_zaal_1",
    "DenHaag_zaal_2",
    "DenHaag_zaal_3",
    "DenHaag_zaal_4",
    "DenHaag_zaal_5",
    "DenHaag_zaal_6",
    "Filmhuis Den Haag 10 (buitenbios)"
]

kw_age = [
    "vanaf 6 jaar",
    "vanaf 9 jaar",
    "vanaf 12 jaar",
    "vanaf 14 jaar",
    "vanaf 18 jaar",
    "Alle leeftijden"
]

kw_keywords = [
    "Angst",
    "Discriminatie",
    "Drugs- en/of alcoholmisbruik",
    "Grof taalgebruik",
    "Gevaarlijk gedrag",
    "Geweld",
    "Seks"
]

attr_extra = [
    "EN subs"
]

sessions: list[Session] = []

for i in range(20):
    start_time = datetime.now(tz=ZoneInfo("Europe/Amsterdam"))+timedelta(minutes=randint(-20, 59))

    attrs = sample(kw_age, 1) + sample(kw_keywords, randint(0, 3)) + sample(attr_extra, randint(0, 1))


    session = Session(
        session_id=randint(1000, 9999),
        screen_identifier=sample(zaal, 1)[0],
        complex_identifier="Filmhuis Den Haag",
        start=start_time,
        end=start_time+timedelta(hours=2),
        feature_duration=int(timedelta(hours=2).total_seconds()),
        title=fake.catch_phrase(),
        rating=randint(1, 10),
        seats_available=100,
        seats_sold=randint(0, 100),
        attributes=attrs
    )
    sessions.append(session)

xml_data = AAMPos(sessions=Sessions(root=sessions))


with open("test_xml.xml", "wb") as f:
    result = xml_data.to_xml(pretty_print=True)
    f.write(result if isinstance(result, bytes) else result.encode("utf-8"))
