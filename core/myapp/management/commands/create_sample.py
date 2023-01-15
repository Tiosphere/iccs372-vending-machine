from random import choices
from typing import Any

from django.core.management.base import BaseCommand
from myapp.models import Machine, Snack, Stock


class Command(BaseCommand):
    help = "Create sample data for testing"

    def handle(self, *args: Any, **options: Any):
        """Use to create sample data"""
        self.stdout.write(self.style.MIGRATE_HEADING("Creating sample data:"))
        if Snack.objects.all().exists():
            self.stdout.write(
                self.style.ERROR("  ERR:") + " You need to call 'manage.py flush' first"
            )
        else:
            snack_list: list[Snack] = Snack.objects.bulk_create(
                [
                    Snack(name=i)
                    for i in [
                        "Water",
                        "Mineral Water",
                        "Coke",
                        "Pepsi",
                        "7-Up",
                        "Fanta",
                        "Coffee",
                        "Green Tea",
                        "Espresso",
                        "Bread",
                        "Sandwich",
                        "Monster",
                    ]
                ]
            )
            machine_list: list[Machine] = Machine.objects.bulk_create(
                [
                    Machine(
                        name=f"Science Building machine {i}",
                        location=f"Science Building {i} floor Mahidol University Salaya",
                    )
                    for i in range(1, 11)
                ]
                + [
                    Machine(
                        name=f"MUIC Building machine {i}",
                        location=f"MUIC Building {i} floor Mahidol University Salaya",
                    )
                    for i in range(1, 11)
                ]
            )
            for i in machine_list:
                for snack in choices(snack_list, k=3):
                    Stock.objects.create(machine=i, snack=snack, quantity=20)
            self.stdout.write("  Finish creating sample data.")
