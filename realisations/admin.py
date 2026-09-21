from django.contrib import admin

from .models import Realisation


@admin.register(Realisation)
class RealisationAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "site_reference", "period_label", "created_at")
    search_fields = ("title", "site_reference", "description")
    list_filter = ("category", "created_at")
