from django.db.models.signals import m2m_changed, pre_delete, pre_save, post_save
from django.dispatch import receiver
from myapp.models import Machine, Stock


@receiver(post_save, sender=Stock)
def machine_status_update(sender, instance: Stock, **kwargs):
    """Keep update vending machine status after edit stock"""
    if not Stock.objects.filter(machine=instance.machine, quantity=0).exists():
        Machine.objects.filter(id=instance.machine.id).update(
            status=Machine.MachineStatus.NORMAL
        )
    else:
        Machine.objects.filter(id=instance.machine.id).update(
            status=Machine.MachineStatus.OUT_OF_STOCK
        )
