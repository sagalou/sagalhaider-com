import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestPublicPages:
    @pytest.mark.parametrize("url_name", ["home", "sites", "cities", "contact"])
    def test_page_renders(self, client, url_name):
        res = client.get(reverse(url_name))
        assert res.status_code == 200
