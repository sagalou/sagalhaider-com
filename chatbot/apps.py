"""App configuration for the chatbot app."""

from django.apps import AppConfig


class ChatbotConfig(AppConfig):
    """Django app config for chatbot."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "chatbot"
