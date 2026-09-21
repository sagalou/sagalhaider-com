import json

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from core.ratelimit import client_ip, is_rate_limited, parse_rate

from .services import ChatbotService


@csrf_exempt
@require_POST
def chatbot_message(request):
    """
    POST /chatbot/message
    No auth, rate-limited by IP.
    JSON in: {message, session_id}
    200: success · 400: empty/malformed · 429: quota exceeded
    502/503: Anthropic API unavailable
    """
    limit, window = parse_rate(settings.RATE_LIMIT_CHATBOT)
    if is_rate_limited(f"chatbot:{client_ip(request)}", limit, window):
        return JsonResponse({"error": "quota exceeded"}, status=429)

    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "malformed JSON"}, status=400)

    message = (payload.get("message") or "").strip()
    if not message:
        return JsonResponse({"error": "empty message"}, status=400)

    service = ChatbotService()
    try:
        result = service.respond(message)
    except Exception as exc:  # Anthropic API error / network issue
        status = getattr(exc, "status_code", 503)
        if status not in (502, 503):
            status = 503
        return JsonResponse({"error": "chatbot temporarily unavailable"}, status=status)

    return JsonResponse(result, status=200)
