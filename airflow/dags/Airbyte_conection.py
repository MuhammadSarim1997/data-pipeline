import requests
import json
import time
import os


def trigger_airbyte_sync():
    # --- Step 0: Define credentials and IDs ---
    client_id = os.getenv("AB_client_id")
    client_secret = os.getenv("AB_client_secret")
    connection_id = os.getenv("AB_connection_id")
    workspace_id = os.getenv("AB_workspace_id")

    # --- Step 1: Get Access Token ---
    print("🔐 Requesting Access Token...")

    token_url = "http://host.docker.internal:8000/api/v1/applications/token"
    token_payload = {
        "client_id": client_id,
        "client_secret": client_secret
    }
    token_headers = {
        "Content-Type": "application/json"
    }

    try:
        token_response = requests.post(token_url, headers=token_headers, json=token_payload)
        token_response.raise_for_status()
        access_token = token_response.json().get("access_token")
    except Exception as e:
        print("❌ Failed to retrieve access token.")
        raise e

    if not access_token:
        raise ValueError("Access token is null or empty.")

    print(f"✅ Access Token: {access_token}")

    # --- Step 2: Trigger Sync ---
    print(f"🔁 Triggering sync for connection: {connection_id}")

    sync_url = "http://host.docker.internal:8000/api/v1/connections/sync"
    sync_payload = {
        "connectionId": connection_id
    }
    sync_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Airbyte-Workspace-Id": workspace_id
    }

    try:
        sync_response = requests.post(sync_url, headers=sync_headers, json=sync_payload)
        sync_response.raise_for_status()
        sync_result = sync_response.json()
        print("📡 Sync Response:")
        # print(json.dumps(sync_response.json(), indent=2))
    except Exception as e:
        print("❌ Failed to trigger sync.")
        raise e

    # Step 3: Poll for job status
    job_id = sync_result["job"]["id"]
    status = "running"
    while status not in ["succeeded", "failed", "cancelled"]:
        time.sleep(10)
        job_info_response = requests.post(
            "http://host.docker.internal:8000/api/v1/jobs/get",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "X-Airbyte-Workspace-Id": workspace_id
            },
            json={"id": job_id}
        ).json()
        print(job_info_response['job']['status'])
        # print(job_info.values())
        status = job_info_response['job']['status']
        print(f"Sync job status: {status}")

    if status != "succeeded":
        raise Exception(f"Airbyte sync failed with status: {status}")


