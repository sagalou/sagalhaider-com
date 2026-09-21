from django.urls import path

from . import views

urlpatterns = [
    path("demandes", views.create_request, name="create-request"),
    path("admin/dashboard", views.admin_dashboard_page, name="admin-dashboard-page"),
    path("admin/demandes", views.admin_requests_list, name="admin-requests-list"),
    path("admin/demandes/<int:request_id>", views.admin_request_detail, name="admin-request-detail"),
    path(
        "admin/demandes/<int:request_id>/etapes/<int:step_id>/complete",
        views.complete_step,
        name="complete-step",
    ),
]
