"""Send a reminder to the admin for requests left unanswered for 7 days."""

from django.core.management.base import BaseCommand

from servicerequests.models import ServiceRequest


class Command(BaseCommand):
    """Check every 'new' request and send a reminder when it is overdue."""

    help = "Send a reminder email for requests still 'new' after 7 days."

    def handle(self, *args, **options):
        """Run check_response_delay() on each pending request."""
        pending = ServiceRequest.objects.filter(
            status=ServiceRequest.STATUS_NEW
        )
        sent = sum(1 for request in pending if request.check_response_delay())
        self.stdout.write(f"{sent} relance(s) envoyée(s).")
