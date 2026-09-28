from django.shortcuts import render

from realisations.models import Realisation


def home(request):
    return render(request, "core/home.html")


def sites(request):
    realisations = Realisation.objects.filter(category=Realisation.CATEGORY_SITE)
    return render(request, "core/gallery.html", {
        "realisations": realisations,
        "category": "site",
        "page_eye": "01 · De la fouille à la vie",
        "page_title": "Reconstitution de sites archéologiques",
        "page_sub": (
            "Rapports de fouilles, relevés de terrain et photogrammétrie pour "
            "reconstituer les sites tels qu'ils étaient, avec rigueur, sans "
            "romantisme."
        ),
        "i18n_eye": "gallery.sites.eye",
        "i18n_title": "gallery.sites.title",
        "i18n_sub": "gallery.sites.sub",
    })


def cities(request):
    realisations = Realisation.objects.filter(category=Realisation.CATEGORY_CITY)
    return render(request, "core/gallery.html", {
        "realisations": realisations,
        "category": "city",
        "page_eye": "02 · Les villes dans le temps",
        "page_title": "Villes d'Afrique de l'Est",
        "page_sub": (
            "Des villes reconstituées à un moment précis de leur histoire, "
            "documentées, modélisées, rendues."
        ),
        "i18n_eye": "gallery.cities.eye",
        "i18n_title": "gallery.cities.title",
        "i18n_sub": "gallery.cities.sub",
    })


def contact(request):
    """Renders the ClientRequestForm page (submission itself goes through
    the JSON /demandes endpoint via fetch, see contact.html)."""
    return render(request, "core/contact.html")