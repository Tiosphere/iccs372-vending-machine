from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Snack(models.Model):
    """Model for all snack name. This model only contain name not stock."""

    id: models.BigAutoField = models.BigAutoField(primary_key=True)
    name: models.CharField = models.CharField(
        max_length=255, editable=True, unique=True
    )

    class Meta:  # noqa: ignore=D106
        ordering = [
            "name",  # Order by name
        ]


class Machine(models.Model):
    """Model for Vending machine contain machine individual information."""

    class MachineStatus(models.TextChoices):
        """
        NORMAL: all working find.

        REFILL: some snacks are out.

        OFFLINE: out of services.
        """

        NORMAL = _("Normal")
        REFILL = _("Refill")
        OFFLINE = _("Offline")

    id: models.BigAutoField = models.BigAutoField(primary_key=True)
    name: models.CharField = models.CharField(
        max_length=255, unique=True, editable=True
    )
    location: models.TextField = models.TextField(
        max_length=500, editable=True, unique=True
    )
    # When create this machine shouldn't have any stock
    status: models.CharField = models.CharField(
        max_length=20,
        choices=MachineStatus.choices,
        default=MachineStatus.OFFLINE,
        editable=True,
    )

    class Meta:  # noqa: ignore=D106
        ordering = [
            "id",  # Order by id
        ]


class Stock(models.Model):
    """Model for stock of vending machine."""

    id: models.BigAutoField = models.BigAutoField(primary_key=True)
    machine: models.ForeignKey = models.ForeignKey(to=Machine, on_delete=models.CASCADE)
    snack: models.ForeignKey = models.ForeignKey(to=Snack, on_delete=models.CASCADE)
    quantity: models.PositiveIntegerField = models.PositiveIntegerField(
        default=0, editable=True
    )

    class Meta:  # noqa: ignore=D106
        ordering = [
            "id",  # Order by id
        ]
        default_related_name = "stock"


class StockLog(models.Model):
    """Model for keeping track of change in stock."""

    id: models.BigAutoField = models.BigAutoField(primary_key=True)
    machine: models.ForeignKey = models.ForeignKey(to=Machine, on_delete=models.CASCADE)
    snack: models.ForeignKey = models.ForeignKey(to=Snack, on_delete=models.CASCADE)
    quantity: models.PositiveIntegerField = models.PositiveIntegerField(
        default=0, editable=True
    )
    created: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:  # noqa: ignore=D106
        ordering = [
            "-created",  # Order by created
        ]
        default_related_name = "stock_log"
