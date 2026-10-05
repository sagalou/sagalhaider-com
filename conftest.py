"""Pytest configuration shared across the test suite."""

import os

import pytest

# Force test-friendly backends before Django settings are loaded, so the
# test suite never needs a real Redis server or SMTP credentials.
os.environ.setdefault("REDIS_DISABLED", "1")
os.environ.setdefault(
    "EMAIL_BACKEND", "django.core.mail.backends.locmem.EmailBackend"
)
os.environ.setdefault("DJANGO_SECRET_KEY", "test-secret-key")


@pytest.fixture(autouse=True)
def clear_ratelimit_cache():
    """Clear the rate-limit cache before and after each test.

    The rate-limit cache is process-global (in-memory or Redis), unlike
    the per-test database, so every test starts from a clean counter --
    otherwise tests bleed rate-limit state into each other.
    """
    from django.core.cache import caches
    caches["ratelimit"].clear()
    yield
    caches["ratelimit"].clear()
