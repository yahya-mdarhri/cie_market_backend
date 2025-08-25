from django.contrib import admin
from django.utils.html import format_html
from .models import Affiliation, Inventor, Ticket, Patent


@admin.register(Affiliation)
class AffiliationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "parent_id")
    search_fields = ("id", "name")
    list_filter = ("parent_id",)
    ordering = ("name",)


@admin.register(Inventor)
class InventorAdmin(admin.ModelAdmin):
    list_display = (
        "preferred_name",
        "email",
        "affiliation",
        "orcid",
        "phone_number",
        "display_image",
        "display_name_variants",
    )
    search_fields = ("preferred_name", "email", "orcid", "old_id")
    list_filter = ("affiliation",)
    ordering = ("preferred_name",)

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="40" height="40" style="object-fit:cover; border-radius:50%;" />', obj.image.url)
        return "-"
    display_image.short_description = "Avatar"

    def display_name_variants(self, obj):
        return ", ".join(obj.name_variants) if obj.name_variants else "-"
    display_name_variants.short_description = "Name Variants"


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "created_at", "meeting_date", "is_draft", "display_co_applications")
    search_fields = ("title", "summary", "context", "problem_identification")
    list_filter = ("status", "is_draft", "created_at")
    filter_horizontal = ("inventors",)
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

    def display_co_applications(self, obj):
        return ", ".join(obj.co_applications) if obj.co_applications else "-"
    display_co_applications.short_description = "Co-applications"


@admin.register(Patent)
class PatentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "deposit_number",
        "status",
        "research_report_result",
        "sector",
        "nature",
        "contract_type",
        "affiliation",
        "display_inventors",
    )
    search_fields = ("title", "deposit_number", "abstract")
    list_filter = (
        "status",
        "research_report_result",
        "contract_type",
        "sector",
        "nature",
        "affiliation",
    )
    filter_horizontal = ("inventors",)
    ordering = ("-deposit_date",)

    def display_inventors(self, obj):
        return ", ".join([inv.preferred_name for inv in obj.inventors.all()])
    display_inventors.short_description = "Inventors"

    def display_schemas(self, obj):
        return ", ".join(obj.schemas) if obj.schemas else "-"
    display_schemas.short_description = "Schemas"
