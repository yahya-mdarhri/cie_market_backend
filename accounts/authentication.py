
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from django.contrib.auth import get_user_model

User = get_user_model()

class TokenAuthentication(JWTAuthentication):
    def authenticate(self, request: Request) -> tuple[User, UntypedToken] | None:
        # Try standard Authorization header first
        header = self.get_header(request)
        if header:
            raw_token = self.get_raw_token(header)
        else:
            # Then try cookie
            raw_token = request.COOKIES.get(settings.AUTH_COOKIE)

        if raw_token is None:
            return None  # No token = unauthenticated

        try:
            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)
        except Exception:
            raise AuthenticationFailed("Invalid or expired token.")

        if not user or not user.is_active:
            raise AuthenticationFailed("User not found or inactive.")

        return user, validated_token