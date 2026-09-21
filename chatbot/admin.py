from django.contrib import admin

from .models import ChatbotRule


@admin.register(ChatbotRule)
class ChatbotRuleAdmin(admin.ModelAdmin):
    list_display = ("keyword",)
    search_fields = ("keyword", "answer")
