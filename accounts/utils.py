import jwt
from django.conf import settings
from datetime import datetime, timedelta, timezone
from rest_framework_simplejwt.tokens import RefreshToken

def generate_jwt_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.now() + timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS),
        'iat': datetime.now(),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload['user_id']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def get_tokens_for_user(user) -> tuple[str, str]:
    refresh = RefreshToken.for_user(user)
    return (str(refresh), str(refresh.access_token))



def store_token_in_cookies(response, token) -> None:
    lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
    expires_at = datetime.now(timezone.utc) + lifetime
    response.set_cookie(
        key=settings.AUTH_COOKIE,
        value=token,
        expires=expires_at,
        httponly=True,
        secure=getattr(settings, 'COOKIE_SECURE', True),
        samesite=getattr(settings, 'COOKIE_SAMESITE', 'None'),
        path='/',
    )