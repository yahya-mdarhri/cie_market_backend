from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import serializers
from .models import InnovationDiagnosisSubmission, MailingListSignup

# Create your views here.

class InnovationDiagnosisSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InnovationDiagnosisSubmission
        fields = ['id', 'name', 'email', 'organisation', 'position', 'phone', 'responses', 'submitted_at']
        read_only_fields = ['id', 'submitted_at']

class InnovationDiagnosisSubmissionView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Submit Innovation Diagnosis answers and user info",
        request_body=InnovationDiagnosisSubmissionSerializer,
        responses={
            201: openapi.Response(description="Submission saved successfully"),
            400: openapi.Response(description="Validation error")
        },
        tags=['public'],
        operation_summary="Submit Innovation Diagnosis",
    )
    def create(self, request):
        serializer = InnovationDiagnosisSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Submission saved successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MailingListSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailingListSignup
        fields = [
            'id', 'first_name', 'last_name', 'email', 'organization', 'job_title', 'role', 'newsletter', 'tech_updates', 'submitted_at'
        ]
        read_only_fields = ['id', 'submitted_at']

class MailingListSignupView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Submit a mailing list signup",
        request_body=MailingListSignupSerializer,
        responses={
            201: openapi.Response(description="Signup saved successfully"),
            400: openapi.Response(description="Validation error")
        },
        tags=['public'],
        operation_summary="Join the mailing list",
    )
    def create(self, request):
        serializer = MailingListSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Signup saved successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
