from django.conf import settings
from rest_framework.views import APIView
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework import (
    status,
    viewsets
)
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken

from .utils import (
    get_tokens_for_user,
    store_token_in_cookies,
)
from .models import User
from .serializers import UserSerializer

# just a view to test auth permissions
class HomeView(viewsets.ViewSet):
    # authentication_classes = []
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response({'message': f'Welcome {user}, to the API!', 'data':serializer.data}, status=status.HTTP_200_OK)


# view endpoint to register a new user
class RegisterView(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# view endpoint to login a new user
class LoginView(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]

    def create(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if email is None or password is None:
            return Response({
                'error': 'Please provide both email and password.'
            }, status=status.HTTP_400_BAD_REQUEST)
        email = email.lower()
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            refresh_token, access_token = get_tokens_for_user(user)
            response = Response({
                'refresh_token': refresh_token,
                'access_token': access_token,
            }, status=status.HTTP_200_OK)
            store_token_in_cookies(response, access_token)
            return response
        return Response({
            'error': 'Please provide the correct email and password.'
        }, status=status.HTTP_404_NOT_FOUND)
    


class LogoutView(viewsets.ViewSet):
    def list(self, request):
        response = Response({"message": "Logged out"})
        response.delete_cookie(settings.AUTH_COOKIE)
        return response