import json
from functools import wraps

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from core.ratelimit import client_ip, is_rate_limited, parse_rate

from .forms import ClientRequestForm
from .models import RequestStep, ServiceRequest


def api_login_required(view):
    """Like login_required, but returns 401 JSON instead of redirecting —
    these are API-style endpoints, not browser pages."""

    @wraps(view)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "session expired"}, status=401)
        return view(request, *args, **kwargs)

    return wrapped


@csrf_exempt
@require_POST
def create_request(request):
    """
    POST /demandes
    No auth. JSON in: {client_nom, client_email, organisation, description_projet}
    201: created · 400: missing/invalid fields · 429: rate limited
    """
    limit, window = parse_rate(settings.RATE_LIMIT_DEMANDES)
    if is_rate_limited(f"demandes:{client_ip(request)}", limit, window):
        return JsonResponse({"error": "too many requests"}, status=429)

    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "invalid JSON"}, status=400)

    form = ClientRequestForm(data={
        "client_name": payload.get("client_nom", ""),
        "client_email": payload.get("client_email", ""),
        "organization": payload.get("organisation", ""),
        "project_description": payload.get("description_projet", ""),
        "website": payload.get("website", ""),  # honeypot
    })

    if not form.is_valid():
        return JsonResponse({"error": "invalid fields", "details": form.errors}, status=400)

    service_request = form.save()
    service_request.send_confirmation()

    return JsonResponse(
        {
            "id": service_request.id,
            "statut": "nouvelle",
            "message": "confirmation envoyée",
        },
        status=201,
    )


@login_required
def admin_dashboard_page(request):
    """HTML shell for the AdminDashboard. Data is loaded client-side from
    the JSON endpoints below (/admin/demandes, /admin/demandes/{id})."""
    return render(request, "servicerequests/dashboard.html")


@api_login_required
@require_GET
def admin_requests_list(request):
    """
    GET /admin/demandes
    Auth required (session). Optional ?statut= filter.
    """
    qs = ServiceRequest.objects.all()
    statut = request.GET.get("statut")
    if statut:
        qs = qs.filter(status=statut)

    data = [
        {
            "id": r.id,
            "client_nom": r.client_name,
            "statut": r.status,
            "created_at": r.created_at.isoformat(),
            "progression": r.progress(),
        }
        for r in qs
    ]
    return JsonResponse(data, safe=False, status=200)


@api_login_required
@require_GET
def admin_request_detail(request, request_id):
    """
    GET /admin/demandes/{id}
    200: success · 401: unauthenticated · 404: not found
    """
    try:
        r = ServiceRequest.objects.get(id=request_id)
    except ServiceRequest.DoesNotExist:
        return JsonResponse({"error": "not found"}, status=404)

    steps = [
        {
            "id": s.id,
            "step_name": s.step_name,
            "is_completed": s.is_completed,
            "order": s.order,
        }
        for s in r.steps.all()
    ]
    return JsonResponse(
        {
            "id": r.id,
            "client_nom": r.client_name,
            "client_email": r.client_email,
            "organisation": r.organization,
            "description_projet": r.project_description,
            "statut": r.status,
            "created_at": r.created_at.isoformat(),
            "progression": r.progress(),
            "etapes": steps,
        },
        status=200,
    )


@api_login_required
@require_POST
def complete_step(request, request_id, step_id):
    """
    POST /admin/demandes/{id}/etapes/{step_id}/complete
    JSON in: {is_completed: true}
    200: updated · 400: invalid field · 401: unauthenticated · 404: not found

    Deliberately NOT csrf_exempt: this is an authenticated admin action, so
    it keeps Django's session CSRF protection. The dashboard's JS sends the
    token via the X-CSRFToken header (see admin_dashboard.html).
    """
    try:
        step = RequestStep.objects.get(id=step_id, request_id=request_id)
    except RequestStep.DoesNotExist:
        return JsonResponse({"error": "not found"}, status=404)

    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "invalid JSON"}, status=400)

    if payload.get("is_completed") is not True:
        return JsonResponse({"error": "invalid field: is_completed must be true"}, status=400)

    step.mark_complete()

    return JsonResponse(
        {
            "step_id": step.id,
            "is_completed": step.is_completed,
            "progression": step.request.progress(),
        },
        status=200,
    )
