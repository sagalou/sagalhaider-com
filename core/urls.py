"""URL routes for the core app."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("sites", views.sites, name="sites"),
    path("cities", views.cities, name="cities"),
    path("a-propos", views.about, name="about"),
    path("a-propos", views.about, name="about"),
    path("contact", views.contact, name="contact"),
]
