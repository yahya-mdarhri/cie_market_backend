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

# Create your views here.
class HomeView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response({'message': 'Welcome to the API!'}, status=status.HTTP_200_OK)

class RegisterView(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(viewsets.ViewSet):
    permission_classes = [AllowAny]
    authentication_classes = []

    def create(self, request):
        email = request.data.get('email').lower()
        password = request.data.get('password')
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
        if not User.objects.filter(username=username).exists():
            return Response({
                'error': 'A user with that username does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
        return Response({
            'error': 'A user with that password does not exist.'
        }, status=status.HTTP_404_NOT_FOUND)
    


class LogoutView(viewsets.ViewSet):
    def list(self, request):
        response = Response({"message": "Logged out"})
        response.delete_cookie(settings.AUTH_COOKIE)
        return response