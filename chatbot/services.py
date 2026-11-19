"""Chatbot response logic: scripted FAQ with an LLM fallback."""

import re

from django.conf import settings

from .models import ChatbotRule

MARKDOWN_RE = re.compile(r"[*#`]+")


class ChatbotService:
    """Encapsulate the API key and call logic.

    Tries the scripted FAQ (ChatbotRule) first — free, zero external
    dependency — and falls back to the Anthropic API for open-ended
    questions.
    """

    SYSTEM_PROMPT = (
        "Tu es l'assistant du site de Sagal Haider, spécialisée en "
        "restitution 3D de sites archéologiques et de villes d'Afrique de "
        "l'Est. Réponds brièvement et avec rigueur, sans inventer de faits "
        "historiques que tu ne connais pas. Réponds en texte brut, sans "
        "markdown : pas d'astérisques, de titres ni de listes à puces."
    )

    def respond(self, message: str) -> dict:
        """Return {"reponse": str, "source": "faq" | "llm"}."""
        rule_answer = ChatbotRule.match(message)
        if rule_answer:
            result = {"reponse": rule_answer, "source": "faq"}
        else:
            result = self._call_anthropic(message)
        result["reponse"] = MARKDOWN_RE.sub("", result["reponse"])
        return result

    def _call_anthropic(self, message: str) -> dict:
        if not settings.ANTHROPIC_API_KEY:
            return {
                "reponse": (
                    "Le chatbot n'est pas configuré pour le moment. "
                    "Contactez-moi directement via le formulaire."
                ),
                "source": "faq",
            }

        import anthropic

        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        response = client.messages.create(
            model=settings.ANTHROPIC_MODEL,
            max_tokens=300,
            system=self.SYSTEM_PROMPT,
            messages=[{"role": "user", "content": message}],
        )
        text = "".join(
            block.text for block in response.content if block.type == "text"
        )
        return {"reponse": text, "source": "llm"}
