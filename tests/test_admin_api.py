# SPDX-FileCopyrightText: 2026 Filmhuis Den Haag
# SPDX-License-Identifier: AGPL-3.0-or-later

from pathlib import Path

from fastapi.testclient import TestClient

from fhdhview.core.config import settings

AUTH = ("username", settings.api_password)


def test_upload_requires_auth(client: TestClient):
    response = client.post("/admin/upload")
    assert response.status_code == 401


def test_upload_requests_wrong_ext(client: TestClient):
    response = client.post(
        "/admin/upload",
        auth=AUTH,
        files={"file": ("test.txt", b"not xml", "text/plain")})
    assert response.status_code == 422


def test_upload_requests_bad_xml(client: TestClient):
    response = client.post(
        "/admin/upload",
        auth=AUTH,
        files={"file": ("test.xml", b"not xml", "application/xml")})
    assert response.status_code == 422


def test_upload_succeeds_with_valid_xml(client: TestClient):
    minimal_xml = Path("tests/data/minimal.xml").read_bytes()
    response = client.post(
        "/admin/upload",
        auth=AUTH,
        files={"file": ("minimal.xml", minimal_xml, "application/xml")})
    assert response.status_code == 200
    assert response.json()['filename'] == "minimal.xml"
