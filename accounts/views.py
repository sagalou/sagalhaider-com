from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

from core.ratelimit import client_ip, is_rate_limited, parse_rate


@csrf_protect
@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    /login
    GET: renders the AdminLoginPage.
    POST: form {username, password}.
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

    login(request, user)
    return redirect(settings.LOGIN_REDIRECT_URL)


def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect("/login")
