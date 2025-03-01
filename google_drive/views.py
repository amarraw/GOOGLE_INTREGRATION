from django.http import JsonResponse
from googleapiclient.discovery import build
from google_drive.drive_service import authenticate_drive, upload_file_to_google_drive, list_google_drive_files



def connect_google_drive(request):
    """Connects to Google Drive and returns a success message."""
    service = authenticate_drive()
    
    if service:
        return JsonResponse({"message": "Successfully connected to Google Drive"})
    
    return JsonResponse({"error": "Failed to connect. Check logs for details."}, status=500)


def upload_file(request):
    """Uploads a file to Google Drive."""
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        file_id = upload_file_to_google_drive(file)
        return JsonResponse({"message": "File uploaded successfully", "file_id": file_id})
    return JsonResponse({"error": "Invalid request"}, status=400)

def list_files(request):
    """Lists files from Google Drive."""
    files = list_google_drive_files()
    return JsonResponse({"files": files})
