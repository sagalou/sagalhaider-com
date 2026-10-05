"""Models for the realisations app (public gallery entries)."""

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
import magic


def validate_video_content_type(file):
    """Check the real MIME type of an uploaded video.

    Checks the actual file content rather than its extension, so a
    malicious file renamed to .mp4 can't slip through.
    """
    allowed_types = ("video/mp4", "video/webm", "video/quicktime")
    file.seek(0)
    detected = magic.from_buffer(file.read(2048), mime=True)
    file.seek(0)
    if detected not in allowed_types:
        raise ValidationError(
            f"Type de fichier non autorisé ({detected}). "
            "Formats acceptés : mp4, webm, mov."
        )


class Realisation(models.Model):
    """A completed or in-progress 3D restitution project.

    Shown in the public gallery (e.g. Beta Samati, an Aksumite basilica).

    Straightforward CRUD via the Django admin — no custom business logic.
    Title/description are stored in French (source language) plus optional
    English and Swahili translations, shown client-side via the site's
    data-i18n mechanism. If a translation is left blank, the French text
    is shown instead.
    """

    CATEGORY_SITE = "site"
    CATEGORY_CITY = "city"
    CATEGORY_CHOICES = [
        (CATEGORY_SITE, "Site archéologique"),
        (CATEGORY_CITY, "Ville d'Afrique de l'Est"),
    ]

    title = models.CharField("titre (français)", max_length=200)
    title_en = models.CharField(
        "titre (anglais)", max_length=200, blank=True,
        help_text="Laisser vide pour afficher le titre français par défaut.",
    )
    title_sw = models.CharField(
        "titre (swahili)", max_length=200, blank=True,
        help_text="Laisser vide pour afficher le titre français par défaut.",
    )
    description = models.TextField("description (français)")
    description_en = models.TextField(
        "description (anglais)", blank=True,
        help_text=(
            "Laisser vide pour afficher la description française "
            "par défaut."
        ),
    )
    description_sw = models.TextField(
        "description (swahili)", blank=True,
        help_text=(
            "Laisser vide pour afficher la description française "
            "par défaut."
        ),
    )
    image = models.ImageField(
        "image / affiche", upload_to="realisations/", blank=True, null=True,
        help_text=(
            "Utilisée comme vignette, et comme image d'affiche "
            "(poster) si une vidéo est fournie."
        ),
    )
    video = models.FileField(
        "vidéo", upload_to="realisations/videos/", blank=True, null=True,
        validators=[
            FileExtensionValidator(["mp4", "webm", "mov"]),
            validate_video_content_type,
        ],
        help_text=(
            "Flyover ou immersion 3D exportée depuis Blender, "
            "Unreal Engine, etc. (mp4/webm/mov)."
        ),
    )
    site_reference = models.CharField(
        "site de référence", max_length=200,
        help_text="Ex : Beta Samati, Gedi, Mogadishu, Aksum",
    )
    category = models.CharField(
        "catégorie", max_length=10, choices=CATEGORY_CHOICES,
        default=CATEGORY_SITE,
    )
    period_label = models.CharField(
        "période", max_length=100, blank=True,
        help_text="Ex : ~1950, IVe siècle",
    )
    created_at = models.DateTimeField("créé le", auto_now_add=True)

    class Meta:
        """Metadata for the Realisation model."""

        verbose_name = "réalisation"
        verbose_name_plural = "réalisations"
        ordering = ["-created_at"]

    def __str__(self):
        """Return the French title as the string representation."""
        return self.title

    @property
    def image_path(self):
        """Return the image URL, or an empty string if none is set."""
        return self.image.url if self.image else ""

    @property
    def video_path(self):
        """Return the video URL, or an empty string if none is set."""
        return self.video.url if self.video else ""

    @property
    def title_en_display(self):
        """Return the English title, falling back to the French one."""
        return self.title_en or self.title

    @property
    def title_sw_display(self):
        """Return the Swahili title, falling back to the French one."""
        return self.title_sw or self.title

    @property
    def description_en_display(self):
        """Return the English description, falling back to French."""
        return self.description_en or self.description

    @property
    def description_sw_display(self):
        """Return the Swahili description, falling back to French."""
        return self.description_sw or self.description
