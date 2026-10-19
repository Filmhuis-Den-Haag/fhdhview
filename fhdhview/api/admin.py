# SPDX-FileCopyrightText: 2026 Filmhuis Den Haag
# SPDX-License-Identifier: AGPL-3.0-or-later

from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse, JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from fhdhview.api.deps import check_auth, get_session
from fhdhview.services.screenwriter.importer import import_sessions
from fhdhview.services.screenwriter.parser import XmlParseError, parse_screenwriter_xml

BASE_DIR = Path(__file__).resolve().parent.parent

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(check_auth)]
)

@router.get("", response_class=FileResponse)
async def upload_form():
    return FileResponse(BASE_DIR / "html" / "upload.html")


@router.post("/upload", response_class=JSONResponse)
async def upload_file(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session)
):
    if not file.filename or not file.filename.lower().endswith(".xml"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="File must be an XML file"
        )

    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File too large"
        )

    try:
        aampos = parse_screenwriter_xml(contents)
    except XmlParseError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(e)
        )

    await import_sessions(aampos, session=session)

    return JSONResponse(content={"filename": file.filename, "size": len(contents)})
