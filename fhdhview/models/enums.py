# SPDX-FileCopyrightText: 2026 Filmhuis Den Haag
# SPDX-License-Identifier: AGPL-3.0-or-later

from enum import Enum


class KijkWijzer(str, Enum):
    ZES = "6"
    NEGEN = "9"
    TWAALF = "12"
    VEERTIEN = "14"
    ZESTIEN = "16"
    ACHTTIEN = "18"
    ALLE = "al"
    ANGST = "angst"
    DISCRIMINATIE = "discriminatie"
    DRUGS = "drugs-en-alcohol"
    GROF = "taal"
    GEDRAG = "gevaarlijk-gedrag"
    GEWELD = "geweld"
    SEKS = "seks"


class Screen(str, Enum):
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    TEN = "10"
