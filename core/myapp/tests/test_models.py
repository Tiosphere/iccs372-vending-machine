from django.test import TestCase
from django.utils import timezone
from myapp.models import Machine, Snack, Stock, StockLog


class TestModel(TestCase):
    def setUp(self):
        self.machine = Machine.objects.create(
            name="new machine", location="new machine location"
        )
        self.snack = Snack.objects.create(name="new snack")

    def test_simple_create(self):
        # ----- machine assert
        self.assertEqual(self.machine.name, "new machine")
        self.assertEqual(self.machine.location, "new machine location")
        self.assertEqual(self.machine.status, Machine.MachineStatus.OFFLINE)
        # ----- snack assert
        self.assertEqual(self.snack.name, "new snack")

    def test_create_stock(self):
        Stock.objects.create(machine=self.machine, snack=self.snack)
        self.assertEqual(self.machine.stock.all().count(), 1)

    def test_machine_status(self):
        stock = Stock.objects.create(machine=self.machine, snack=self.snack)
        self.assertEqual(self.machine.status, Machine.MachineStatus.OFFLINE)
        # update stock
        stock.quantity = 10
        stock.save()
        self.machine.refresh_from_db()  # update instance
        self.assertEqual(self.machine.status, Machine.MachineStatus.NORMAL)
        # add new out of stock snack
        Stock.objects.create(
            machine=self.machine, snack=Snack.objects.create(name="temp snack")
        )
        self.machine.refresh_from_db()
        self.assertEqual(self.machine.status, Machine.MachineStatus.REFILL)

    def test_stock_log(self):
        self.assertEqual(StockLog.objects.all().count(), 0)
        # create first stock
        stock = Stock.objects.create(machine=self.machine, snack=self.snack)
        stock_log = StockLog.objects.all().first()
        self.assertEqual(StockLog.objects.all().count(), 1)
        self.assertLessEqual(stock_log.created, timezone.now())
        self.assertEqual(stock_log.machine, self.machine)
        self.assertEqual(stock_log.snack, self.snack)
        self.assertEqual(stock_log.quantity, 0)
        # edit quantity
        stock.quantity = 10
        stock.save()
        stock_log = StockLog.objects.all().first()
        self.assertEqual(StockLog.objects.all().count(), 2)
        self.assertLessEqual(stock_log.created, timezone.now())
        self.assertEqual(stock_log.machine, self.machine)
        self.assertEqual(stock_log.snack, self.snack)
        self.assertEqual(stock_log.quantity, 10)
