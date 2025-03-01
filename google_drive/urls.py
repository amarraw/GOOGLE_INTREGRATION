from django.urls import path
from .views import connect_google_drive, upload_file, list_files

urlpatterns = [
    path("connect/", connect_google_drive, name="connect_google_drive"),
    path("upload/", upload_file, name="upload_file"),
    path("list/", list_files, name="list_files"),
]
