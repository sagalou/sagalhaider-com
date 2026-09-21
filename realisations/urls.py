from django.urls import path

from . import views

urlpatterns = [
    path("", views.realisations_list, name="realisations-list"),
]
