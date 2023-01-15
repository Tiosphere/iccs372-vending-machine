from typing import Any
from django.core import management
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Auto migrate and create sample data"

    def handle(self, *args: Any, **options: Any):
        management.call_command("migrate")
        management.call_command("create_sample")
