"""URL routes for the chatbot app."""

from django.urls import path

from . import views

urlpatterns = [
    path("message", views.chatbot_message, name="chatbot-message"),
]
