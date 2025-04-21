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
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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

    @swagger_auto_schema(
        operation_description="Get current authenticated user's data",
        responses={
            200: openapi.Response(
                description="Authenticated user data",
                schema=UserSerializer()
            ),
            401: 'Unauthorized - User is not authenticated'
        },
        tags=['User'],
    )
    def retrieve(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# view endpoint to register a new user
# class RegisterView(viewsets.ViewSet):
#     authentication_classes = []
#     permission_classes = [AllowAny]

#     @swagger_auto_schema(
#         operation_description="Register a new user with email and password",
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             required=['email', 'password', 'inventor'],
#             properties={
#                 'email': openapi.Schema(type=openapi.TYPE_STRING, format='email'),
#                 'password': openapi.Schema(type=openapi.TYPE_STRING, format='password'),
#                 'inventor': openapi.Schema(type=openapi.TYPE_STRING),
#             },
#         ),
#         responses={
#             201: openapi.Response(
#                 description="User registered successfully",
#                 examples={
#                     "application/json": {
#                         "message": "User registered successfully",
#                         "user": {
#                             "id": 1,
#                             "email": "user@example.com",
#                             "first_name": "John",
#                             "last_name": "Doe"
#                         }
#                     }
#                 }
#             ),
#             400: openapi.Response(description="Validation error")
#         },
#         tags=['Authentication'],
#         operation_summary="Register a new user",
#     )
#     def create(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# view endpoint to login a new user
class LoginView(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]


    @swagger_auto_schema(
        operation_description="Login user and return access + refresh tokens",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format='email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format='password'),
            },
        ),
        responses={
            200: openapi.Response("Success", schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                    'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )),
            400: 'Invalid credentials',
        },
        tags=['Authentication'],
        operation_summary="Login user",
    )
    def create(self, request):
        email = request .data.get('email')
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
                "message": "Login successful",
                'refresh_token': refresh_token,
                'access_token': access_token,
            }, status=status.HTTP_200_OK)
            store_token_in_cookies(response, access_token)
            return response
        return Response({
            'error': 'Please provide the correct email and password.'
        }, status=status.HTTP_400_BAD_REQUEST)
    


class LogoutView(viewsets.ViewSet):
    @swagger_auto_schema(
    operation_description="Logout user by deleting auth cookie",
        responses={
            200: openapi.Response(description="Logged out")
        },
        tags=['Authentication'],
        operation_summary="Login out",
    )
    def retrieve(self, request):
        response = Response({"message": "Logged out"})
        response.delete_cookie(settings.AUTH_COOKIE)
        return response