"""Admin registration for the servicerequests app."""

from django.contrib import admin

from .models import RequestStep, ServiceRequest


class RequestStepInline(admin.TabularInline):
    """Inline editor for a ServiceRequest's steps."""

    model = RequestStep
    extra = 1


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    """Admin interface for ServiceRequest."""

    list_display = (
        "client_name", "client_email", "status", "created_at", "admin",
    )
    list_filter = ("status",)
    search_fields = ("client_name", "client_email", "organization")
    inlines = [RequestStepInline]


@admin.register(RequestStep)
class RequestStepAdmin(admin.ModelAdmin):
    """Admin interface for RequestStep."""

    list_display = ("request", "step_name", "is_completed", "order")
    list_filter = ("is_completed",)
