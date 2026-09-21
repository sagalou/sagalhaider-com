import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse


@pytest.mark.django_db
class TestLogin:
    @pytest.fixture
    def staff_user(self):
        return get_user_model().objects.create_user(
            username="admin", password="testpass123", is_staff=True,
        )

    def test_get_renders_login_page(self, client):
        res = client.get(reverse("login"))
        assert res.status_code == 200

    def test_valid_credentials_redirect(self, client, staff_user):
        res = client.post(reverse("login"), {"username": "admin", "password": "testpass123"})
        assert res.status_code == 302
        assert res.url == "/admin/dashboard"

    def test_invalid_credentials_return_401(self, client, staff_user):
        res = client.post(reverse("login"), {"username": "admin", "password": "wrong"})
        assert res.status_code == 401

    def test_non_staff_user_rejected(self, client):
        get_user_model().objects.create_user(username="bob", password="testpass123", is_staff=False)
        res = client.post(reverse("login"), {"username": "bob", "password": "testpass123"})
        assert res.status_code == 401

    def test_rate_limited_after_threshold(self, client, staff_user, settings):
        settings.RATE_LIMIT_LOGIN = "1/h"
        client.post(reverse("login"), {"username": "admin", "password": "wrong"})
        res = client.post(reverse("login"), {"username": "admin", "password": "wrong"})
        assert res.status_code == 429
