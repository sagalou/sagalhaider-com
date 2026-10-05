"""Admin registration for the chatbot app."""

from django.contrib import admin

from .models import ChatbotRule


@admin.register(ChatbotRule)
class ChatbotRuleAdmin(admin.ModelAdmin):
    """Admin interface for ChatbotRule."""

    list_display = ("keyword",)
    search_fields = ("keyword", "answer")
