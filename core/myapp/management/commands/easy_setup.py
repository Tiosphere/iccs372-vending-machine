from typing import Any

from django.core import management
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Command to run all setup command and process."""

    help = "Auto migrate and create sample data"

    def handle(self, *args: Any, **options: Any):
        """Run all command process here."""
        management.call_command("migrate")
        management.call_command("create_sample")
