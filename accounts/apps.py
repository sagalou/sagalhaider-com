"""App configuration for the accounts app."""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Django app config for accounts."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
