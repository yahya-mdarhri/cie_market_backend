from django.contrib import admin
from django.utils.html import format_html
from django.utils.text import Truncator
from .models import InnovationDiagnosisSubmission, MailingListSignup, ContactSubmission


@admin.register(InnovationDiagnosisSubmission)
class InnovationDiagnosisSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "organization", "position", "user_type", "submitted_at", "display_responses")
    list_filter = ("user_type", "submitted_at")
    search_fields = ("name", "email", "organization", "position")
    readonly_fields = ("submitted_at",)
    ordering = ("-submitted_at",)

    def display_responses(self, obj):
        if obj.responses:
            return Truncator(str(obj.responses)).chars(50)
        return "-"
    display_responses.short_description = "Responses"



@admin.register(MailingListSignup)
class MailingListSignupAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "organization", "job_title", "newsletter", "tech_updates", "submitted_at")
    list_filter = ("newsletter", "tech_updates", "submitted_at")
    search_fields = ("first_name", "last_name", "email", "organization", "job_title", "role")
    readonly_fields = ("submitted_at",)
    ordering = ("-submitted_at",)



@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "contact_type", "company_name", "position", "subject", "display_message", "submitted_at")
    list_filter = ("contact_type", "submitted_at")
    search_fields = ("name", "email", "phone", "company_name", "subject", "message")
    readonly_fields = ("submitted_at",)
    ordering = ("-submitted_at",)

    def display_message(self, obj):
        return Truncator(obj.message).chars(50)
    display_message.short_description = "Message"
