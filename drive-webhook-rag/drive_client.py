import os
import io
import json
import logging
from pathlib import Path
from datetime import datetime, timezone

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from config import (
    CREDENTIALS_FILE,
    TOKEN_FILE,
    WATCHED_FOLDER_ID,
    DOWNLOADS_DIR,
    PAGE_TOKEN_FILE,
)

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


def get_drive_service():
    """Authenticate and return a Drive API service instance."""
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return build("drive", "v3", credentials=creds)


def _load_page_token():
    if os.path.exists(PAGE_TOKEN_FILE):
        with open(PAGE_TOKEN_FILE) as f:
            return json.load(f).get("token")
    return None


def _save_page_token(token: str):
    with open(PAGE_TOKEN_FILE, "w") as f:
        json.dump({"token": token}, f)


def init_page_token():
    """
    Call this once at startup to grab the current changes page token,
    so we only process files added AFTER the server starts.
    """
    service = get_drive_service()
    resp = service.changes().getStartPageToken().execute()
    token = resp.get("startPageToken")
    _save_page_token(token)
    logger.info(f"Initialized page token: {token}")
    return token


def get_changed_files() -> list[dict]:
    """
    Poll the Drive Changes API using our saved page token.
    Returns only files that are in the watched folder, not trashed.
    """
    service = get_drive_service()
    page_token = _load_page_token()

    if not page_token:
        logger.warning("No page token found — call init_page_token() first.")
        return []

    changed_files = []

    while page_token:
        resp = service.changes().list(
            pageToken=page_token,
            spaces="drive",
            fields="nextPageToken,newStartPageToken,changes(file(id,name,mimeType,parents,trashed))",
        ).execute()

        for change in resp.get("changes", []):
            file = change.get("file", {})
            if not file or file.get("trashed"):
                continue
            parents = file.get("parents", [])
            if WATCHED_FOLDER_ID in parents:
                changed_files.append(file)

        page_token = resp.get("nextPageToken")
        if "newStartPageToken" in resp:
            _save_page_token(resp["newStartPageToken"])

    return changed_files


def download_file(file_id: str, file_name: str, mime_type: str) -> str | None:
    """
    Download a file from Drive to the local downloads directory.
    Returns the local file path, or None if the type is unsupported.
    """
    service = get_drive_service()
    DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)

    # Google Workspace files need export
    export_map = {
        "application/vnd.google-apps.document": (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".docx",
        ),
        "application/vnd.google-apps.spreadsheet": (
            "text/csv",
            ".csv",
        ),
    }

    supported_native = {
        "application/pdf": ".pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
        "text/plain": ".txt",
        "text/csv": ".csv",
        "text/markdown": ".md",
    }

    local_path = None

    if mime_type in export_map:
        export_mime, ext = export_map[mime_type]
        safe_name = Path(file_name).stem + ext
        local_path = DOWNLOADS_DIR / safe_name
        request = service.files().export_media(fileId=file_id, mimeType=export_mime)
    elif mime_type in supported_native:
        ext = supported_native[mime_type]
        safe_name = Path(file_name).stem + ext
        local_path = DOWNLOADS_DIR / safe_name
        request = service.files().get_media(fileId=file_id)
    else:
        logger.info(f"Unsupported MIME type: {mime_type}")
        return None

    buffer = io.BytesIO()
    downloader = MediaIoBaseDownload(buffer, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()

    with open(local_path, "wb") as f:
        f.write(buffer.getvalue())

    logger.info(f"Downloaded to {local_path}")
    return str(local_path)