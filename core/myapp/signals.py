from django.db.models.signals import m2m_changed, pre_delete, pre_save, post_save
from django.dispatch import receiver
from myapp.models import Machine, Stock


@receiver(post_save, sender=Stock)
def machine_status_update(sender, instance: Stock, **kwargs):
    """Keep update vending machine status after edit stock"""
    query = Stock.objects.filter(machine=instance.machine)
    all: int = query.count()
    out: int = query.filter(quantity=0).count()
    if not out:
        Machine.objects.filter(id=instance.machine.id).update(
            status=Machine.MachineStatus.NORMAL
        )
    elif out == all:
        Machine.objects.filter(id=instance.machine.id).update(
            status=Machine.MachineStatus.OFFLINE
        )
    else:
        Machine.objects.filter(id=instance.machine.id).update(
            status=Machine.MachineStatus.REFILL
        )
