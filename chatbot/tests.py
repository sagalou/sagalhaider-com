import json

import pytest
from django.urls import reverse

from .models import ChatbotRule


@pytest.mark.django_db
class TestChatbotEndpoint:
    def test_empty_message_returns_400(self, client):
        res = client.post(
            reverse("chatbot-message"), data=json.dumps({"message": ""}),
            content_type="application/json",
        )
        assert res.status_code == 400

    def test_malformed_json_returns_400(self, client):
        res = client.post(
            reverse("chatbot-message"), data="not json", content_type="application/json",
        )
        assert res.status_code == 400

    def test_faq_rule_matched_before_llm(self, client):
        ChatbotRule.objects.create(keyword="beta samati", answer="C'est une basilique aksoumite.")
        res = client.post(
            reverse("chatbot-message"),
            data=json.dumps({"message": "Dis-moi tout sur Beta Samati", "session_id": "s1"}),
            content_type="application/json",
        )
        assert res.status_code == 200
        body = res.json()
        assert body["source"] == "faq"
        assert "basilique" in body["reponse"]

    def test_no_matching_rule_and_no_api_key_falls_back_gracefully(self, client, settings):
        settings.ANTHROPIC_API_KEY = ""
        res = client.post(
            reverse("chatbot-message"),
            data=json.dumps({"message": "Question sans règle", "session_id": "s1"}),
            content_type="application/json",
        )
        assert res.status_code == 200
        assert res.json()["source"] == "faq"

    def test_rate_limited_after_threshold(self, client, settings):
        settings.RATE_LIMIT_CHATBOT = "1/h"
        payload = json.dumps({"message": "salut", "session_id": "s1"})
        res = client.post(reverse("chatbot-message"), data=payload, content_type="application/json")
        assert res.status_code == 200
        res = client.post(reverse("chatbot-message"), data=payload, content_type="application/json")
        assert res.status_code == 429


@pytest.mark.django_db
class TestChatbotRuleModel:
    def test_match_is_case_insensitive(self):
        ChatbotRule.objects.create(keyword="Aksum", answer="réponse aksum")
        assert ChatbotRule.match("parle-moi d'aksum") == "réponse aksum"

    def test_no_match_returns_none(self):
        assert ChatbotRule.match("bonjour") is None
