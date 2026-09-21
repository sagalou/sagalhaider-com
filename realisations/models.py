from django.db import models


class Realisation(models.Model):
    """
    A completed or in-progress 3D restitution project shown in the public
    gallery (e.g. Beta Samati, an Aksumite basilica).

    Straightforward CRUD via the Django admin — no custom business logic.
    """

    CATEGORY_SITE = "site"
    CATEGORY_CITY = "city"
    CATEGORY_CHOICES = [
        (CATEGORY_SITE, "Site archéologique"),
        (CATEGORY_CITY, "Ville d'Afrique de l'Est"),
    ]

    title = models.CharField("titre", max_length=200)
    description = models.TextField("description")
    image = models.ImageField("image", upload_to="realisations/", blank=True, null=True)
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
