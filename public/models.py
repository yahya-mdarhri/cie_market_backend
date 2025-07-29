import uuid
from django.db import models

# Create your models here.

import uuid

class InnovationDiagnosisSubmission(models.Model):
    USER_TYPE_CHOICES = [
        ('person', 'Person'),
        ('company', 'Company'),
    ]
  
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    organization = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='person')
    info_questions = models.JSONField(null=True, blank=True)
    responses = models.JSONField()
    profile_responses = models.JSONField(null=True, blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'innovation_diagnosis_submissions'
        ordering = ['-submitted_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['submitted_at']),
        ]

class MailingListSignup(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    organization = models.CharField(max_length=150, blank=True)
    job_title = models.CharField(max_length=150, blank=True)
    role = models.CharField(max_length=100, blank=True)
    newsletter = models.BooleanField(default=False)
    tech_updates = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mailing_list_signups'
        ordering = ['-submitted_at']
