from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), "credentials.json")


def authenticate_drive():
    """Authenticates and returns a Google Drive API service instance."""
    try:
        if not os.path.exists(CREDENTIALS_PATH):
            print("❌ credentials.json file not found!")
            return None
        
        credentials = service_account.Credentials.from_service_account_file(
            CREDENTIALS_PATH, scopes=["https://www.googleapis.com/auth/drive"]
        )
        service = build("drive", "v3", credentials=credentials)
        return service
    except Exception as e:
        print(f"❌ Error authenticating Google Drive: {e}")
        return None

def upload_file_to_google_drive(file):
    """Uploads a file to Google Drive."""
    service = authenticate_drive()
    
    file_metadata = {"name": file.name}
    media = MediaFileUpload(file.temporary_file_path(), mimetype=file.content_type)

    file_drive = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    return file_drive.get("id")

def list_google_drive_files():
    """Lists files from Google Drive."""
    service = authenticate_drive()
    results = service.files().list().execute()
    return results.get("files", [])
