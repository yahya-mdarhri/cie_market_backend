
from django.contrib import admin
from .models import InnovationDiagnosisSubmission, MailingListSignup, ContactSubmission


@admin.register(InnovationDiagnosisSubmission)
class InnovationDiagnosisSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "organization", "position", "user_type", "submitted_at")
    list_filter = ("user_type", "submitted_at")
    search_fields = ("name", "email", "organization", "position")
    ordering = ("-submitted_at",)


@admin.register(MailingListSignup)
class MailingListSignupAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "organization", "newsletter", "tech_updates", "submitted_at")
    list_filter = ("newsletter", "tech_updates", "submitted_at")
    search_fields = ("first_name", "last_name", "email", "organization", "job_title", "role")
    ordering = ("-submitted_at",)


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "contact_type", "company_name", "position", "subject", "submitted_at")
    list_filter = ("contact_type", "submitted_at")
    search_fields = ("name", "email", "phone", "company_name", "subject", "message")
    ordering = ("-submitted_at",)
