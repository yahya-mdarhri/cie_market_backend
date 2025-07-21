from django.db import models

# Create your models here.

class InnovationDiagnosisSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    organisation = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    responses = models.JSONField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'innovation_diagnosis_submissions'
        ordering = ['-submitted_at']

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
