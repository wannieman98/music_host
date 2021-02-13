from .models import SptifyToken
from django.utils import timezone
from datetime import timedelta
from requests import post
from dotenv import load_dotenv
from os import getenv

load_dotenv()

def get_user_tokens(session_id):
    user_tokens = SptifyToken.objects.filter(user=session_id)
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None


def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token):
    tokens = get_user_tokens(session_id)
    if expires_in:
        expires_in = timezone.now() + timedelta(seconds=expires_in)
    else:
        expires_in = timezone.now() + timedelta(seconds=3600)

    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token, refresh_token', 'expires_in', 'token_type'])
    else:
        tokens = SptifyToken(user=session_id, access_token=access_token,
                             expires_in=expires_in, token_type=token_type, refresh_token=refresh_token)
        tokens.save()

def is_spotify_autenticated(session_id):
    tokens = get_user_tokens(session_id)
    if tokens:
        expiry = tokens.expires_in
        if expiry <= timezone.now():
            refresh_spotify_token(session_id)

        return True

    
    return False

def refresh_spotify_token(session_id):
    refresh_token = get_user_tokens(session_id).refresh_token

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': getenv("clientId"),
        'client_secret': getenv("clientSecret")
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    refresh_token = response.get('refresh_token')

    update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token)


