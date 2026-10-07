"""Tests for the accounts app (admin login)."""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django_otp.oath import TOTP
from django_otp.plugins.otp_totp.models import TOTPDevice


@pytest.mark.django_db
class TestLogin:
    """Tests for the /login endpoint."""

    @pytest.fixture
    def staff_user(self):
        """Create and return a staff user."""
        return get_user_model().objects.create_user(
            username="admin", password="testpass123", is_staff=True,
        )

    @pytest.fixture
    def totp_device(self, staff_user):
        """Create and return a confirmed TOTP device for the staff user."""
        return TOTPDevice.objects.create(
            user=staff_user, name="phone", confirmed=True,
        )

    @staticmethod
    def current_token(device):
        """Return the 6-digit code the authenticator app would show now."""
        totp = TOTP(device.bin_key, device.step, device.t0, device.digits)
        return f"{totp.token():0{device.digits}d}"

    def test_get_renders_login_page(self, client):
        """GET /login renders the login page."""
        res = client.get(reverse("login"))
        assert res.status_code == 200

    def test_valid_credentials_and_code_redirect(
        self, client, totp_device,
    ):
        """Valid password and 2FA code redirect to the admin dashboard."""
        res = client.post(reverse("login"), {
            "username": "admin", "password": "testpass123",
            "otp_token": self.current_token(totp_device),
        })
        assert res.status_code == 302
        assert res.url == "/admin/dashboard"

    def test_missing_code_returns_401(self, client, totp_device):
        """A correct password without the 2FA code is refused."""
        res = client.post(
            reverse("login"),
            {"username": "admin", "password": "testpass123"},
        )
        assert res.status_code == 401

    def test_wrong_code_returns_401(self, client, totp_device):
        """A correct password with a wrong 2FA code is refused."""
        res = client.post(reverse("login"), {
            "username": "admin", "password": "testpass123",
            "otp_token": "000000",
        })
        assert res.status_code == 401

    def test_invalid_credentials_return_401(self, client, staff_user):
        """Wrong password returns 401."""
        res = client.post(
            reverse("login"), {"username": "admin", "password": "wrong"}
        )
        assert res.status_code == 401

    def test_non_staff_user_rejected(self, client):
        """A non-staff user cannot log in to the admin."""
        get_user_model().objects.create_user(
            username="bob", password="testpass123", is_staff=False
        )
        res = client.post(
            reverse("login"), {"username": "bob", "password": "testpass123"}
        )
        assert res.status_code == 401

    def test_rate_limited_after_threshold(self, client, staff_user, settings):
        """Repeated login attempts past the limit return 429."""
        settings.RATE_LIMIT_LOGIN = "1/h"
        client.post(
            reverse("login"), {"username": "admin", "password": "wrong"}
        )
        res = client.post(
            reverse("login"), {"username": "admin", "password": "wrong"}
        )
        assert res.status_code == 429
