from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
import requests
from django.contrib.auth.models import User

def google_login(request):
    google_auth_url = "https://accounts.google.com/o/oauth2/auth"
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account",
    }
    auth_url = f"{google_auth_url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"
    return redirect(auth_url)


def google_callback(request):
    code = request.GET.get("code")

    if not code:
        return JsonResponse({"error": "Authorization code not provided"}, status=400)

    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    token_response = requests.post(token_url, data=token_data).json()
    access_token = token_response.get("access_token")

    if not access_token:
        return JsonResponse({"error": "Failed to retrieve access token"}, status=400)

    user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    user_info_response = requests.get(
        user_info_url, headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    email = user_info_response.get("email")
    first_name = user_info_response.get("given_name", "")
    last_name = user_info_response.get("family_name", "")

    user, created = User.objects.get_or_create(email=email, defaults={
        "username": email,
        "first_name": first_name,
        "last_name": last_name,
    })

    return JsonResponse({
        "message": "User authenticated successfully",
        "user": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        },
    })