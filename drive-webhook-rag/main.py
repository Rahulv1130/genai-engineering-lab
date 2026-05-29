import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

from drive_client import get_changed_files, download_file
from embedder import embed_and_store
from watcher import renew_watch_if_needed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Drive Auto-Embedder")



@app.post("/webhook/drive")
async def drive_webhook(request: Request):
    """
    Google Drive push notification endpoint.
    Drive sends a POST with headers describing the change;
    we fetch the actual changed files via the Drive API.
    """
    headers = request.headers

    # Google sends a sync message on channel creation — ignore it
    resource_state = headers.get("X-Goog-Resource-State", "")
    if resource_state == "sync":
        logger.info("Received sync message from Drive — ignoring.")
        return JSONResponse(status_code=200, content={"status": "sync acknowledged"})

    if resource_state not in ("add", "update", "change"):
        return JSONResponse(status_code=200, content={"status": "ignored"})

    logger.info(f"Drive change detected (state={resource_state}), fetching changed files...")

    try:
        changed_files = get_changed_files()
        for file_meta in changed_files:
            file_id = file_meta["id"]
            file_name = file_meta["name"]
            mime_type = file_meta.get("mimeType", "")

            logger.info(f"Processing: {file_name} ({file_id})")
            local_path = download_file(file_id, file_name, mime_type)

            if local_path:
                embed_and_store(local_path, file_meta)
                logger.info(f"Embedded and stored: {file_name}")
            else:
                logger.warning(f"Skipped unsupported file: {file_name} [{mime_type}]")

        # Renew the watch channel before it expires (1 week max)
        renew_watch_if_needed()

    except Exception as e:
        logger.error(f"Error processing webhook: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

    return JSONResponse(status_code=200, content={"status": "ok"})


@app.get("/health")
def health():
    return {"status": "running"}