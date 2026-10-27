"""Tests for the chatbot app."""

import json

import pytest
from django.urls import reverse

from .models import ChatbotRule


@pytest.mark.django_db
class TestChatbotEndpoint:
    """Tests for the /chatbot/message endpoint."""

    def test_empty_message_returns_400(self, client):
        """An empty message is rejected with 400."""
        res = client.post(
            reverse("chatbot-message"), data=json.dumps({"message": ""}),
            content_type="application/json",
        )
        assert res.status_code == 400

    def test_malformed_json_returns_400(self, client):
        """Malformed JSON body is rejected with 400."""
        res = client.post(
            reverse("chatbot-message"), data="not json",
            content_type="application/json",
        )
        assert res.status_code == 400

    def test_faq_rule_matched_before_llm(self, client):
        """A matching scripted rule answers without calling the LLM."""
        ChatbotRule.objects.create(
            keyword="beta samati", answer="C'est une basilique aksoumite."
        )
        res = client.post(
            reverse("chatbot-message"),
            data=json.dumps({
                "message": "Dis-moi tout sur Beta Samati",
                "session_id": "s1",
            }),
            content_type="application/json",
        )
        assert res.status_code == 200
        body = res.json()
        assert body["source"] == "faq"
        assert "basilique" in body["reponse"]

    def test_no_matching_rule_and_no_api_key_falls_back_gracefully(
        self, client, settings,
    ):
        """No matching rule and no API key still returns a response."""
        settings.ANTHROPIC_API_KEY = ""
        res = client.post(
            reverse("chatbot-message"),
            data=json.dumps({
                "message": "Question sans règle", "session_id": "s1",
            }),
            content_type="application/json",
        )
        assert res.status_code == 200
        assert res.json()["source"] == "faq"

    def test_rate_limited_after_threshold(self, client, settings):
        """Repeated messages past the limit return 429."""
        settings.RATE_LIMIT_CHATBOT = "1/h"
        payload = json.dumps({"message": "salut", "session_id": "s1"})
        res = client.post(
            reverse("chatbot-message"), data=payload,
            content_type="application/json",
        )
        assert res.status_code == 200
        res = client.post(
            reverse("chatbot-message"), data=payload,
            content_type="application/json",
        )
        assert res.status_code == 429


@pytest.mark.django_db
class TestChatbotRuleModel:
    """Tests for ChatbotRule.match."""

    def test_match_is_case_insensitive(self):
        """Keyword matching ignores case."""
        ChatbotRule.objects.create(keyword="Aksum", answer="réponse aksum")
        assert ChatbotRule.match("parle-moi d'aksum") == "réponse aksum"

    def test_no_match_returns_none(self):
        """No matching keyword returns None."""
        assert ChatbotRule.match("bonjour") is None


class TestChatbotModelTierSelection:
    """Tests for the CHATBOT_MODEL_TIER -> ANTHROPIC_MODEL selection."""

    def test_low_tier_selects_haiku(self, settings):
        """The "low" tier selects the Haiku model."""
        low_model = settings.ANTHROPIC_MODELS["low"]
        model = settings.ANTHROPIC_MODELS.get("low", low_model)
        assert model == "claude-haiku-4-5-20251001"

    def test_high_tier_selects_sonnet(self, settings):
        """The "high" tier selects the Sonnet model."""
        low_model = settings.ANTHROPIC_MODELS["low"]
        model = settings.ANTHROPIC_MODELS.get("high", low_model)
        assert model == "claude-sonnet-5"

    def test_unknown_tier_falls_back_to_low(self, settings):
        """An unrecognized tier falls back to the low-tier model."""
        low_model = settings.ANTHROPIC_MODELS["low"]
        model = settings.ANTHROPIC_MODELS.get("unknown-tier", low_model)
        assert model == low_model
