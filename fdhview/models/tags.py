from fdhview.models.enums import KijkWijzer, Screen

screens = {
    'DenHaag_zaal_1': Screen.ONE,
    'DenHaag_zaal_2': Screen.TWO,
    'DenHaag_zaal_3': Screen.THREE,
    'DenHaag_zaal_4': Screen.FOUR,
    'DenHaag_zaal_5': Screen.FIVE,
    'DenHaag_zaal_6': Screen.SIX,
    'Filmhuis Den Haag 10 (buitenbios)': Screen.TEN
}


kijkwijzer = {
    'vanaf 6 jaar': KijkWijzer.ZES,
    'vanaf 9 jaar': KijkWijzer.NEGEN,
    'vanaf 12 jaar': KijkWijzer.TWAALF,
    'vanaf 14 jaar': KijkWijzer.VEERTIEN,
    'vanaf 16 jaar': KijkWijzer.ZESTIEN,
    'vanaf 18 jaar': KijkWijzer.ACHTTIEN,
    'Alle leeftijden': KijkWijzer.ALLE,
    'Angst': KijkWijzer.ANGST,
    'Discriminatie': KijkWijzer.DISCRIMINATIE,
    'Drugs- en/of alcoholmisbruik': KijkWijzer.DRUGS,
    'Grof taalgebruik': KijkWijzer.GROF,
    'Gevaarlijk gedrag': KijkWijzer.GEDRAG,
    'Geweld': KijkWijzer.GEWELD,
    'Seks': KijkWijzer.SEKS
}


extra_tags = [
    '2D',
    'Action',
    'Adventure',
    'Animation',
    'Biographie',
    'Comedy',
    'Crime',
    'Documentary',
    'Drama',
    'EN subs',
    'Family film',
    'Family',
    'Fantasy',
    'Festival',
    'Horror',
    'Kids film',
    'Kids',
    'LGBTQ+',
    'Met muziek',
    'Romantic',
    'Science fiction',
    'Sciencefiction',
    'Thriller',
    'Voorfilm',
    'War',
    'with after talk',
    'with introduction'
]
