
from rest_framework import serializers
from .models import InnovationDiagnosisSubmission, MailingListSignup

class InnovationDiagnosisSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InnovationDiagnosisSubmission
        fields = ['__all__']
        read_only_fields = ['id', 'submitted_at']


class MailingListSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailingListSignup
        fields = ['__all__']
        read_only_fields = ['id', 'submitted_at']