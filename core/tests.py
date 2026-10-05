"""Tests for the core app's public pages."""

import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestPublicPages:
    """Tests that each public page renders successfully."""

    @pytest.mark.parametrize(
        "url_name", ["home", "sites", "cities", "contact"]
    )
    def test_page_renders(self, client, url_name):
        """Each public page returns 200."""
        res = client.get(reverse(url_name))
        assert res.status_code == 200
