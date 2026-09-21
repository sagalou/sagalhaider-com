from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import Realisation


@require_GET
def realisations_list(request):
    """
    GET /realisations
    No auth. Returns JSON list: {id, titre, description, image_path, site_reference}
    """
    data = [
        {
            "id": r.id,
            "titre": r.title,
            "description": r.description,
            "image_path": r.image_path,
            "site_reference": r.site_reference,
            "category": r.category,
            "period_label": r.period_label,
        }
        for r in Realisation.objects.all()
    ]
    return JsonResponse(data, safe=False, status=200)
