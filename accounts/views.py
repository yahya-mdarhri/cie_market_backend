from django.conf import settings
from rest_framework.views import APIView
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework import (
    status,
    viewsets,
    permissions
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from .utils import (
    get_tokens_for_user,
    store_token_in_cookies,
)
from .models import User
from .serializers import UserSerializer

class UserMeView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get current user's details",
        responses={200: openapi.Response(description="User details", schema=UserSerializer())},
        tags=['User'],
        operation_summary="Get current user",
    )
    def retrieve(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update current user's details",
        request_body=UserSerializer,
        responses={200: openapi.Response(description="User updated", schema=UserSerializer())},
        tags=['User'],
        operation_summary="Update current user",
    )
    def update(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @swagger_auto_schema(
    #     operation_description="Partially update current user's details",
    #     request_body=UserSerializer,
    #     responses={200: openapi.Response(description="User updated", schema=UserSerializer())},
    #     tags=['User'],
    #     operation_summary="Partial update current user",
    # )
    # def partial_update(self, request):
    #     serializer = UserSerializer(request.user, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


class RegisterView(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new user with email and password",
        request_body=UserSerializer(),
        responses={
            201: openapi.Response(
                description="User registered successfully",
                examples={
                    "application/json": {
                        "message": "User registered successfully",
                        "user": {
                            "id": 1,
                            "email": "user@example.com",
                            "first_name": "John",
                            "last_name": "Doe"
                        }
                    }
                }
            ),
            400: openapi.Response(description="Validation error")
        },
        tags=['Authentication'],
        operation_summary="Register a new user",
    )
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


class ChangePasswordView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Change the password for the logged-in user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['old_password', 'new_password'],
            properties={
                'old_password': openapi.Schema(type=openapi.TYPE_STRING, format='password'),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, format='password'),
            },
        ),
        responses={
            200: openapi.Response(description="Password changed successfully"),
            400: openapi.Response(description="Old password is incorrect"),
        },
        tags=['User'],
        operation_summary="Change password",
    )
    def create(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if not user.check_password(old_password):
            return Response({'detail': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
        user.password = (make_password(new_password))
        user.save()
        return Response({'detail': 'Password changed successfully.'})

class ResetPasswordView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Send password reset email to user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format='email'),
            },
        ),
        responses={
            200: openapi.Response(description="Password reset email sent"),
            404: openapi.Response(description="User not found"),
            400: openapi.Response(description="Email is required"),
        },
        tags=['Authentication'],
        operation_summary="Reset password",
    )
    def create(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.id))
        reset_link = f"http://localhost:8000/accounts/reset-password-confirm/{uid}/{token}/"
        send_mail(
            'Password Reset Request',
            f'Click the link to reset your password: {reset_link}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)

class ResetPasswordConfirmView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Confirm password reset with token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['new_password'],
            properties={
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, format='password'),
            },
        ),
        responses={
            200: openapi.Response(description="Password reset successful"),
            400: openapi.Response(description="Invalid token or user"),
        },
        tags=['Authentication'],
        operation_summary="Confirm password reset",
    )
    def create(self, request, uidb64=None, token=None):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Invalid user.'}, status=status.HTTP_400_BAD_REQUEST)
        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
        new_password = request.data.get('new_password')
        if not new_password:
            return Response({'error': 'New password is required.'}, status=status.HTTP_400_BAD_REQUEST)
        user.password = make_password(new_password)
        user.save()
        return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)