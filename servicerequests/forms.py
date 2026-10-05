"""Forms for the servicerequests app."""

from django import forms

from .models import ServiceRequest


class ClientRequestForm(forms.ModelForm):
    """Public-facing request form with a honeypot anti-spam field."""

    # Honeypot: real users never see or fill this (hidden via CSS in the
    # template); bots that auto-fill every field will trip it.
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        """Metadata for the ClientRequestForm."""

        model = ServiceRequest
        fields = [
            "client_name", "client_email", "organization",
            "project_description",
        ]
        widgets = {
            "project_description": forms.Textarea(attrs={"rows": 5}),
        }

    def clean_website(self):
        """Reject submissions where the honeypot field was filled in."""
        value = self.cleaned_data.get("website")
        if value:
            raise forms.ValidationError("Spam détecté.")
        return value
