# SPDX-FileCopyrightText: 2026 Filmhuis Den Haag
# SPDX-License-Identifier:

from datetime import datetime
from pathlib import Path

import pytest

from fdhview.services.screenwriter.importer import _clean_title
from fdhview.services.screenwriter.schema import AAMPos


def test_xml():
    xml = Path('tests/data/minimal.xml').read_text()
    data = AAMPos.from_xml(xml)

    sessions = data.sessions.root

    assert isinstance(sessions[1].start, datetime)
    assert isinstance(sessions[1].end, datetime)
    assert len(sessions[1].attributes) == 5
    assert len(sessions[2].attributes) == 2


def test_broken_xml():
    xml = Path('tests/data/broken.xml').read_text()
    with pytest.raises(ValueError):
        AAMPos.from_xml(xml)


def test_clean_title():
        # Basic cases
        assert _clean_title("Good Movie - EN subs") == "Good Movie"
        assert _clean_title("Good Movie- EN subs") == "Good Movie"
        assert _clean_title("Good Movie - en subs") == "Good Movie"
        assert _clean_title("Good Movie - NL sub") == "Good Movie"

        # Presentation / talk variations
        assert _clean_title("Good Movie - met inleiding") == "Good Movie"
        assert _clean_title("Good Movie - met inleiding en nagesprek") == "Good Movie"
        assert _clean_title("Good Movie – met nagesprek") == "Good Movie"
        assert _clean_title("Good Movie - met voorfilms en nagesprek") == "Good Movie"
        assert _clean_title("Good Movie - EN subs met inleiding") == "Good Movie"

        # Stacked suffixes
        assert _clean_title("Good Movie - met inleiding - EN subs") == "Good Movie"

        # Titles that should NOT be modified
        assert _clean_title("Good Movie") == "Good Movie"
        assert _clean_title("De la Comédie-Française") == "De la Comédie-Française"
        assert _clean_title("Dikkie Dik (re-release)") == "Dikkie Dik (re-release)"
        assert _clean_title("Aguirre - Epic Summer - EN subs") == "Aguirre - Epic Summer"
