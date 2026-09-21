import pytest
from django.urls import reverse

from .models import Realisation


@pytest.mark.django_db
class TestRealisationEndpoint:
    def test_empty_list(self, client):
        res = client.get(reverse("realisations-list"))
        assert res.status_code == 200
        assert res.json() == []

    def test_lists_created_realisations(self, client):
        Realisation.objects.create(
            title="Beta Samati",
            description="Basilique aksoumite",
            site_reference="Beta Samati",
            category=Realisation.CATEGORY_SITE,
        )
        res = client.get(reverse("realisations-list"))
        assert res.status_code == 200
        data = res.json()
        assert len(data) == 1
        assert data[0]["titre"] == "Beta Samati"
        assert data[0]["site_reference"] == "Beta Samati"

    def test_only_get_allowed(self, client):
        res = client.post(reverse("realisations-list"))
        assert res.status_code == 405
