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


@pytest.fixture
def otp_login():
    """Return a helper that logs a user in with a verified 2FA device.

    It creates a confirmed TOTP device for the user, logs them in, and
    marks the session as OTP-verified, as a real 2FA login would.
    """
    from django_otp import DEVICE_ID_SESSION_KEY
    from django_otp.plugins.otp_totp.models import TOTPDevice

    def _login(client, user):
        device = TOTPDevice.objects.create(
            user=user, name="test", confirmed=True,
        )
        client.force_login(user)
        session = client.session
        session[DEVICE_ID_SESSION_KEY] = device.persistent_id
        session.save()
        return device

    return _login
