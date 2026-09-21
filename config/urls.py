"""
URL mapping matching the Stage 3 endpoint spec:

/realisations                                          -> realisations app
/demandes                                               -> servicerequests app
/login                                                  -> accounts app
/admin/demandes[...]                                    -> servicerequests app
/chatbot/message                                        -> chatbot app
/django-admin/                                          -> Django's own admin site
                                                            (moved off /admin/ since the
                                                             project's own admin dashboard
                                                             lives at /admin/demandes)
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core import views as core_views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("", include("core.urls")),
    path("realisations", include("realisations.urls")),
    path("", include("servicerequests.urls")),
    path("", include("accounts.urls")),
    path("chatbot/", include("chatbot.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
