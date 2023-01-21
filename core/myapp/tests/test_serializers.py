from typing import Any

from django.test import TestCase
from myapp.models import Machine, Snack, Stock
from myapp.serializers import (
    machine_detail_serializer,
    machine_serializer,
    snack_serializer,
    stock_serializer,
)


class TestSnackSerializer(TestCase):
    def setUp(self):
        self.name = "new snack"
        self.instance = Snack.objects.create(name=self.name)

    def test_simple(self):
        serialize_instance: dict[str, Any] = snack_serializer(self.instance)
        self.assertEqual(serialize_instance.get("id"), self.instance.id)
        self.assertEqual(serialize_instance.get("name"), self.name)


class TestMachineSerializer(TestCase):
    def setUp(self):
        self.name = "new machine"
        self.location = "new machine location"
        self.instance = Machine.objects.create(name=self.name, location=self.location)

    def test_simple(self):
        serialize_instance: dict[str, Any] = machine_serializer(self.instance)
        self.assertEqual(serialize_instance.get("id"), self.instance.id)
        self.assertEqual(serialize_instance.get("name"), self.name)
        self.assertEqual(serialize_instance.get("location"), self.location)
        self.assertEqual(serialize_instance.get("status"), Machine.MachineStatus.OFFLINE)
        self.assertEqual(serialize_instance.get("stock"), None)


class TestMachineDetailAndStockSerializer(TestCase):
    def setUp(self):
        self.machine_name = "new machine"
        self.machine_location = "new machine location"
        self.machine_instance = Machine.objects.create(
            name=self.machine_name, location=self.machine_location
        )
        self.snack_name = "new snack"
        self.snack_instance = Snack.objects.create(name=self.snack_name)
        self.snack_quantity = 20
        self.stock_instance = Stock.objects.create(
            machine=self.machine_instance,
            snack=self.snack_instance,
            quantity=self.snack_quantity,
        )
        self.machine_instance.refresh_from_db()

    def test_stock(self):
        serialize_instance: dict[str, Any] = stock_serializer(self.stock_instance)
        self.assertEqual(serialize_instance.get("snack_id"), self.snack_instance.id)
        self.assertEqual(serialize_instance.get("snack_name"), self.snack_name)
        self.assertEqual(serialize_instance.get("quantity"), self.snack_quantity)

    def test_machine_detail(self):
        serialize_instance: dict[str, Any] = machine_detail_serializer(
            self.machine_instance
        )
        self.assertEqual(serialize_instance.get("id"), self.machine_instance.id)
        self.assertEqual(serialize_instance.get("name"), self.machine_name)
        self.assertEqual(serialize_instance.get("location"), self.machine_location)
        self.assertEqual(serialize_instance.get("status"), Machine.MachineStatus.NORMAL)
        self.assertEqual(
            serialize_instance.get("stock")[0],
            stock_serializer(self.machine_instance.stock.first()),
        )
