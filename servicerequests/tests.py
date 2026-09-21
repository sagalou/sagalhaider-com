import json

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import RequestStep, ServiceRequest


@pytest.mark.django_db
class TestCreateRequest:
    def test_valid_submission_returns_201(self, client):
        res = client.post(
            reverse("create-request"),
            data=json.dumps({
                "client_nom": "Jean Test",
                "client_email": "jean@test.com",
                "organisation": "Musée X",
                "description_projet": "Restitution 3D d'un site",
            }),
            content_type="application/json",
        )
        assert res.status_code == 201
        body = res.json()
        assert body["statut"] == "nouvelle"
        assert ServiceRequest.objects.count() == 1

    def test_missing_fields_returns_400(self, client):
        res = client.post(
            reverse("create-request"), data=json.dumps({}), content_type="application/json",
        )
        assert res.status_code == 400

    def test_honeypot_rejects_bots(self, client):
        res = client.post(
            reverse("create-request"),
            data=json.dumps({
                "client_nom": "Bot",
                "client_email": "bot@test.com",
                "description_projet": "spam",
                "website": "http://spam.example",
            }),
            content_type="application/json",
        )
        assert res.status_code == 400
        assert ServiceRequest.objects.count() == 0

    def test_rate_limited_after_threshold(self, client, settings):
        settings.RATE_LIMIT_DEMANDES = "2/h"
        payload = json.dumps({
            "client_nom": "X", "client_email": "x@x.com", "description_projet": "test",
        })
        for _ in range(2):
            res = client.post(reverse("create-request"), data=payload, content_type="application/json")
            assert res.status_code == 201
        res = client.post(reverse("create-request"), data=payload, content_type="application/json")
        assert res.status_code == 429


@pytest.mark.django_db
class TestAdminEndpoints:
    @pytest.fixture
    def staff_user(self):
        return get_user_model().objects.create_user(
            username="admin", password="testpass123", is_staff=True,
        )

    @pytest.fixture
    def a_request(self):
        req = ServiceRequest.objects.create(
            client_name="Client A", client_email="a@a.com", project_description="Projet A",
        )
        RequestStep.objects.create(request=req, step_name="Devis", order=1)
        return req

    def test_list_requires_auth(self, client):
        res = client.get(reverse("admin-requests-list"))
        assert res.status_code == 401

    def test_list_returns_data_when_authenticated(self, client, staff_user, a_request):
        client.force_login(staff_user)
        res = client.get(reverse("admin-requests-list"))
        assert res.status_code == 200
        assert res.json()[0]["client_nom"] == "Client A"

    def test_detail_404_for_unknown_id(self, client, staff_user):
        client.force_login(staff_user)
        res = client.get(reverse("admin-request-detail", args=[9999]))
        assert res.status_code == 404

    def test_complete_step_updates_progress(self, client, staff_user, a_request):
        client.force_login(staff_user)
        step = a_request.steps.first()
        res = client.post(
            reverse("complete-step", args=[a_request.id, step.id]),
            data=json.dumps({"is_completed": True}),
            content_type="application/json",
        )
        assert res.status_code == 200
        assert res.json()["progression"] == 100
        step.refresh_from_db()
        assert step.is_completed is True

    def test_complete_step_rejects_bad_payload(self, client, staff_user, a_request):
        client.force_login(staff_user)
        step = a_request.steps.first()
        res = client.post(
            reverse("complete-step", args=[a_request.id, step.id]),
            data=json.dumps({"is_completed": "not-a-bool"}),
            content_type="application/json",
        )
        assert res.status_code == 400


@pytest.mark.django_db
class TestServiceRequestModel:
    def test_progress_with_no_steps_is_zero(self):
        req = ServiceRequest.objects.create(
            client_name="A", client_email="a@a.com", project_description="x",
        )
        assert req.progress() == 0

    def test_progress_counts_completed_steps(self):
        req = ServiceRequest.objects.create(
            client_name="A", client_email="a@a.com", project_description="x",
        )
        RequestStep.objects.create(request=req, step_name="1", order=1, is_completed=True)
        RequestStep.objects.create(request=req, step_name="2", order=2, is_completed=False)
        assert req.progress() == 50
