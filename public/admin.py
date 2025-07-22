from django.contrib import admin
from .models import InnovationDiagnosisSubmission, MailingListSignup

@admin.register(InnovationDiagnosisSubmission)
class InnovationDiagnosisSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'organisation', 'position', 'submitted_at')
    list_filter = ('submitted_at',)
    search_fields = ('name', 'email', 'organisation')
    readonly_fields = ('submitted_at',)
    ordering = ('-submitted_at',)

@admin.register(MailingListSignup)
class MailingListSignupAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'organization', 'job_title', 'role', 'newsletter', 'tech_updates', 'submitted_at')
    list_filter = ('newsletter', 'tech_updates', 'role', 'submitted_at')
    search_fields = ('first_name', 'last_name', 'email', 'organization')
    readonly_fields = ('submitted_at',)
    ordering = ('-submitted_at',)
