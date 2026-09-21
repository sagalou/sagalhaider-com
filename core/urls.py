from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("sites", views.sites, name="sites"),
    path("cities", views.cities, name="cities"),
    path("contact", views.contact, name="contact"),
]
