"""Models for the chatbot app."""

from django.db import models


class ChatbotRule(models.Model):
    """A scripted FAQ entry, tried before falling back to the LLM."""

    keyword = models.CharField("mot-clé", max_length=100)
    answer = models.TextField("réponse")

    class Meta:
        """Metadata for the ChatbotRule model."""

        verbose_name = "règle chatbot"
        verbose_name_plural = "règles chatbot"

    def __str__(self):
        """Return the rule's keyword as the string representation."""
        return self.keyword

    @classmethod
    def match(cls, user_message: str):
        """Return the answer of the first rule matching the message.

        A rule matches when its keyword appears in the user's message
        (case-insensitive). Returns None if nothing matches.
        """
        message = user_message.lower()
        for rule in cls.objects.all():
            if rule.keyword.lower() in message:
                return rule.answer
        return None
