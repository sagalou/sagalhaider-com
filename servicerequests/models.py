from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone


class ServiceRequest(models.Model):
    """A client's request for a 3D restitution project, tracked through
    admin-managed steps until completion."""

    STATUS_NEW = "new"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_COMPLETED = "completed"
    STATUS_CHOICES = [
        (STATUS_NEW, "Nouvelle"),
        (STATUS_IN_PROGRESS, "En cours"),
        (STATUS_COMPLETED, "Terminée"),
    ]

    client_name = models.CharField("nom du client", max_length=200)
    client_email = models.EmailField("email du client")
    organization = models.CharField("organisation", max_length=200, blank=True)
    project_description = models.TextField("description du projet")
    status = models.CharField(
        "statut", max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW
    )
    created_at = models.DateTimeField("créée le", auto_now_add=True)
    last_reminder_sent_at = models.DateTimeField(
        "dernière relance envoyée le", null=True, blank=True
    )
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="responsable",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_requests",
    )

    class Meta:
        verbose_name = "demande"
        verbose_name_plural = "demandes"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.client_name} — {self.get_status_display()}"

    def send_confirmation(self):
        """Send the confirmation email to the client on submission."""
        send_mail(
            subject="Votre demande a bien été reçue — Sagal Haider",
            message=(
                f"Bonjour {self.client_name},\n\n"
                "Votre demande de projet a bien été reçue et sera traitée "
                "dans les meilleurs délais.\n\n"
                f"Résumé : {self.project_description}\n\n"
                "— Sagal Haider"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.client_email],
            fail_silently=True,
        )

    def check_response_delay(self):
        """Trigger a reminder email if more than 7 days without a status
        update (i.e. still 'new'), and record when it was sent."""
        if self.status != self.STATUS_NEW:
            return False
        stale_since = self.last_reminder_sent_at or self.created_at
        if timezone.now() - stale_since < timedelta(days=7):
            return False
        send_mail(
            subject="Relance — demande en attente",
            message=(
                f"La demande de {self.client_name} ({self.client_email}) "
                f"est toujours au statut 'nouvelle' depuis plus de 7 jours."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=True,
        )
        self.last_reminder_sent_at = timezone.now()
        self.save(update_fields=["last_reminder_sent_at"])
        return True

    def progress(self) -> int:
        """Percentage of completed steps, for dashboard display."""
        steps = self.steps.all()
        if not steps:
            return 0
        completed = sum(1 for s in steps if s.is_completed)
        return round(100 * completed / len(steps))


class RequestStep(models.Model):
    """One step in the tracked progress of a ServiceRequest."""

    request = models.ForeignKey(
        ServiceRequest, on_delete=models.CASCADE, related_name="steps"
    )
    step_name = models.CharField("étape", max_length=200)
    is_completed = models.BooleanField("terminée", default=False)
    order = models.PositiveIntegerField("ordre", default=0)
    completed_at = models.DateTimeField("terminée le", null=True, blank=True)

    class Meta:
        verbose_name = "étape"
        verbose_name_plural = "étapes"
        ordering = ["order"]

    def __str__(self):
        return f"{self.request.client_name} — {self.step_name}"

    def mark_complete(self):
        self.is_completed = True
        self.completed_at = timezone.now()
        self.save(update_fields=["is_completed", "completed_at"])
