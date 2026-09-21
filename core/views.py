from django.shortcuts import render

from realisations.models import Realisation


def home(request):
    return render(request, "core/home.html")


def sites(request):
    realisations = Realisation.objects.filter(category=Realisation.CATEGORY_SITE)
    return render(request, "core/gallery.html", {
        "realisations": realisations,
        "page_eye": "01 · From dig to life",
        "page_title": "Reconstitution de sites archéologiques",
        "page_sub": (
            "Rapports de fouilles, relevés de terrain et photogrammétrie pour "
            "reconstituer les sites tels qu'ils étaient — avec rigueur, sans "
            "romanticisme."
        ),
    })


def cities(request):
    realisations = Realisation.objects.filter(category=Realisation.CATEGORY_CITY)
    return render(request, "core/gallery.html", {
        "realisations": realisations,
        "page_eye": "02 · Cities in time",
        "page_title": "Villes d'Afrique de l'Est",
        "page_sub": (
            "Des villes reconstituées à un moment précis de leur histoire — "
            "documentées, modélisées, rendues."
        ),
    })


def contact(request):
    """Renders the ClientRequestForm page (submission itself goes through
    the JSON /demandes endpoint via fetch, see contact.html)."""
    return render(request, "core/contact.html")
