import logging
from drive_client import init_page_token
from watcher import register_watch

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    print("Step 1: Authenticating with Google Drive...")
    token = init_page_token()
    print(f"  Page token saved: {token}")

    print("\nStep 2: Registering webhook with Google Drive...")
    state = register_watch()
    print(f"  Channel ID : {state['channel_id']}")
    print(f"  Resource ID: {state['resource_id']}")
    print(f"  Expires    : {state['expiry_ms']}")

    print("\nSetup complete! Start the server with:")
    print("  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")