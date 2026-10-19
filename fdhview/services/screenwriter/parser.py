# SPDX-FileCopyrightText: 2026 Filmhuis Den Haag
# SPDX-License-Identifier:

from xml.etree import ElementTree as ET

from pydantic import ValidationError

from fdhview.services.screenwriter.schema import AAMPos


class XmlParseError(Exception):
    """Raised when an XML is malformed or violates the ScreenWriter schema."""


def parse_screenwriter_xml(content: bytes | str) -> AAMPos:
    """Parser raw ScreenWriter XML into validated Pydantic models."""
    try:
        return AAMPos.from_xml(content)
    except (ValidationError, ET.ParseError) as e:
        raise XmlParseError(f"Failed to parse ScreenWriter XML: {e}") from e
