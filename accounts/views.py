"""Views for the accounts app (admin login and logout)."""

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django_otp import login as otp_login
from django_otp import match_token

from core.ratelimit import client_ip, is_rate_limited, parse_rate


@csrf_protect
@require_http_methods(["GET", "POST"])
def login_view(request):
    """Handle GET/POST for /login.

    GET: renders the AdminLoginPage.
    POST: form {username, password, otp_token}.
    302: success (redirect + session cookie) · 401: invalid credentials
    429: too many attempts
    """
    if request.method == "GET":
        return render(request, "accounts/login.html")

    limit, window = parse_rate(settings.RATE_LIMIT_LOGIN)
    if is_rate_limited(f"login:{client_ip(request)}", limit, window):
        return JsonResponse({"error": "too many attempts"}, status=429)

    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    user = authenticate(request, username=username, password=password)

    if user is None or not user.is_staff:
        return render(
            request, "accounts/login.html",
            {"error": "Identifiants invalides."}, status=401,
        )

    token = request.POST.get("otp_token", "").strip()
    device = match_token(user, token) if token else None
    if device is None:
        return render(
            request, "accounts/login.html",
            {"error": "Code de vérification invalide."}, status=401,
        )

    login(request, user)
    otp_login(request, device)
    return redirect(settings.LOGIN_REDIRECT_URL)


def logout_view(request):
    """Log the current user out and redirect to /login."""
    from django.contrib.auth import logout
    logout(request)
    return redirect("/login")
