import uuid
import json
import logging
import os
from datetime import datetime, timezone, timedelta

from drive_client import get_drive_service
from config import WATCHED_FOLDER_ID, WEBHOOK_URL, CHANNEL_STATE_FILE

logger = logging.getLogger(__name__)

# Drive push channels expire after ~1 week (604800 seconds max)
CHANNEL_TTL_SECONDS = 6 * 24 * 3600  # renew after 6 days to be safe


def _load_channel_state() -> dict:
    if os.path.exists(CHANNEL_STATE_FILE):
        with open(CHANNEL_STATE_FILE) as f:
            return json.load(f)
    return {}


def _save_channel_state(state: dict):
    with open(CHANNEL_STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def register_watch():
    """
    Register a Drive push notification channel on the watched folder.
    Call this once when the server starts up.
    """
    service = get_drive_service()
    channel_id = str(uuid.uuid4())

    body = {
        "id": channel_id,
        "type": "web_hook",
        "address": WEBHOOK_URL,
    }

    print("REGISTERING WEBHOOK:", WEBHOOK_URL)

    # Watch all changes (file additions trigger a 'change' on the folder)
    response = service.changes().watch(
        pageToken=_get_start_token(service),
        body=body,
    ).execute()
    
    print(f"Regsiter Watch Response : {response}")

    expiry_ms = int(response.get("expiration", 0))
    state = {
        "channel_id": channel_id,
        "resource_id": response.get("resourceId"),
        "expiry_ms": expiry_ms,
        "registered_at": datetime.now(timezone.utc).isoformat(),
        "address": WEBHOOK_URL
    }
    _save_channel_state(state)
    logger.info(f"Watch registered. Channel: {channel_id}, expires: {datetime.fromtimestamp(expiry_ms/1000, tz=timezone.utc)}")
    return state


def _get_start_token(service) -> str:
    from config import PAGE_TOKEN_FILE
    if os.path.exists(PAGE_TOKEN_FILE):
        with open(PAGE_TOKEN_FILE) as f:
            return json.load(f).get("token", "1")
    resp = service.changes().getStartPageToken().execute()
    return resp.get("startPageToken", "1")


def stop_watch():
    """Stop the current watch channel (useful on server shutdown)."""
    state = _load_channel_state()
    if not state:
        return

    service = get_drive_service()
    try:
        service.channels().stop(body={
            "id": state["channel_id"],
            "resourceId": state["resource_id"],
        }).execute()
        logger.info("Watch channel stopped.")
    except Exception as e:
        logger.warning(f"Could not stop channel: {e}")


def renew_watch_if_needed():
    """Renew the watch channel if it's expiring within 24 hours."""
    state = _load_channel_state()
    if not state:
        logger.info("No channel state found, registering fresh watch.")
        register_watch()
        return

    expiry_ms = state.get("expiry_ms", 0)
    expiry_dt = datetime.fromtimestamp(expiry_ms / 1000, tz=timezone.utc)
    time_left = expiry_dt - datetime.now(timezone.utc)

    if time_left < timedelta(hours=24):
        logger.info("Channel expiring soon — renewing.")
        stop_watch()
        register_watch()
    else:
        logger.debug(f"Channel still valid for {time_left}")