from django.core.validators import FileExtensionValidator
from django.db import models


class Realisation(models.Model):
    """
    A completed or in-progress 3D restitution project shown in the public
    gallery (e.g. Beta Samati, an Aksumite basilica).

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
        help_text="Laisser vide pour afficher la description française par défaut.",
    )
    description_sw = models.TextField(
        "description (swahili)", blank=True,
        help_text="Laisser vide pour afficher la description française par défaut.",
    )
    image = models.ImageField(
        "image / affiche", upload_to="realisations/", blank=True, null=True,
        help_text="Utilisée comme vignette, et comme image d'affiche (poster) si une vidéo est fournie.",
    )
    video = models.FileField(
        "vidéo", upload_to="realisations/videos/", blank=True, null=True,
        validators=[FileExtensionValidator(["mp4", "webm", "mov"])],
        help_text="Flyover ou immersion 3D exportée d'Unreal Engine (mp4/webm/mov).",
    )
    site_reference = models.CharField(
        "site de référence", max_length=200,
        help_text="Ex : Beta Samati, Gedi, Mogadishu, Aksum",
    )
    category = models.CharField(
        "catégorie", max_length=10, choices=CATEGORY_CHOICES, default=CATEGORY_SITE,
    )
    period_label = models.CharField(
        "période", max_length=100, blank=True,
        help_text="Ex : ~1950, IVe siècle",
    )
    created_at = models.DateTimeField("créé le", auto_now_add=True)

    class Meta:
        verbose_name = "réalisation"
        verbose_name_plural = "réalisations"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def image_path(self):
        return self.image.url if self.image else ""

    @property
    def video_path(self):
        return self.video.url if self.video else ""

    @property
    def title_en_display(self):
        return self.title_en or self.title

    @property
    def title_sw_display(self):
        return self.title_sw or self.title

    @property
    def description_en_display(self):
        return self.description_en or self.description

    @property
    def description_sw_display(self):
        return self.description_sw or self.description