"""Admin registration for the realisations app."""

from django.contrib import admin

from .models import Realisation


@admin.register(Realisation)
class RealisationAdmin(admin.ModelAdmin):
    """Admin interface for Realisation."""

    list_display = (
        "title", "category", "site_reference", "period_label", "created_at",
    )
    search_fields = ("title", "site_reference", "description")
    list_filter = ("category", "created_at")

    fieldsets = (
        ("Contenu principal (français)", {
            "fields": (
                "title", "description", "image", "video",
                "site_reference", "category", "period_label",
            ),
        }),
        ("Traduction anglaise (optionnelle)", {
            "classes": ("collapse",),
            "fields": ("title_en", "description_en"),
        }),
        ("Traduction swahili (optionnelle)", {
            "classes": ("collapse",),
            "fields": ("title_sw", "description_sw"),
        }),
    )
