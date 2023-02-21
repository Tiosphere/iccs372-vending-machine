from django.db.models.manager import BaseManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from myapp.models import Machine, Stock, StockLog


@receiver(post_save, sender=Stock)
def machine_status_update(sender: BaseManager[Stock], instance: Stock, **kwargs):
    """Keep update vending machine status after edit stock."""
    query = Stock.objects.filter(machine=instance.machine)
    all_stock: int = query.count()
    out_stock: int = query.filter(quantity=0).count()
    if not out_stock:
        Machine.objects.filter(id=instance.machine.id).update(
            status=Machine.MachineStatus.NORMAL
        )
    elif out_stock == all_stock:
        Machine.objects.filter(id=instance.machine.id).update(
            status=Machine.MachineStatus.OFFLINE
        )
    else:
        Machine.objects.filter(id=instance.machine.id).update(
            status=Machine.MachineStatus.REFILL
        )


@receiver(post_save, sender=Stock)
def stock_log(sender: BaseManager[Stock], instance: Stock, **kwargs):
    """Create new log every time stock get updated."""
    StockLog.objects.create(
        machine=instance.machine, snack=instance.snack, quantity=instance.quantity
    )
