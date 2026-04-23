import os
from pathlib import Path


def upload_to_drive(package_path: str, run_id: str) -> str | None:
    credentials_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID")

    if not credentials_path or not folder_id:
        return None

    try:
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload

        creds = Credentials.from_service_account_file(
            credentials_path,
            scopes=["https://www.googleapis.com/auth/drive"],
        )
        service = build("drive", "v3", credentials=creds, cache_discovery=False)

        # Create a run subfolder inside the target Drive folder
        folder_meta = {
            "name": f"darkroom_post_{run_id}",
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [folder_id],
        }
        created = service.files().create(body=folder_meta, fields="id,webViewLink").execute()
        subfolder_id = created["id"]
        drive_url = created.get("webViewLink", "")

        _MIME = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".json": "application/json",
            ".txt": "text/plain",
        }

        for file_path in sorted(Path(package_path).iterdir()):
            if not file_path.is_file():
                continue
            mime = _MIME.get(file_path.suffix.lower(), "application/octet-stream")
            service.files().create(
                body={"name": file_path.name, "parents": [subfolder_id]},
                media_body=MediaFileUpload(str(file_path), mimetype=mime),
            ).execute()

        return drive_url

    except Exception as exc:
        print(f"  Drive upload error: {exc}")
        return None
