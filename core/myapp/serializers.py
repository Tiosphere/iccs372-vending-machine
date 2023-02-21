from typing import Any

from myapp.models import Machine, Snack, Stock, StockLog


def snack_serializer(instance: Snack) -> dict[str, Any]:
    """Create json format of snack."""
    return {"id": instance.id, "name": instance.name}


def stock_serializer(instance: Stock) -> dict[str, Any]:
    """Create json format of stock."""
    return {
        "snack_id": instance.snack.id,
        "snack_name": instance.snack.name,
        "quantity": instance.quantity,
    }


def stock_log_serializer(instance: StockLog) -> dict[str, Any]:
    """Create json format of stock log."""
    return {
        "snack_id": instance.snack.id,
        "machine_id": instance.machine.id,
        "quantity": instance.quantity,
        "created": str(instance.created),
    }


def machine_serializer(instance: Machine) -> dict[str, Any]:
    """Create json format of vending machine without stock detail."""
    return {
        "id": instance.id,
        "name": instance.name,
        "location": instance.location,
        "status": instance.status,
    }


def machine_detail_serializer(instance: Machine) -> dict[str, Any]:
    """Create json format of vending machine with stock detail."""
    return {
        "id": instance.id,
        "name": instance.name,
        "location": instance.location,
        "status": instance.status,
        "stock": [
            stock_serializer(i) for i in instance.stock.all().select_related("snack")
        ],
    }


def json_format(result: Any = None, error: bool = False) -> dict[str, Any]:
    """Make sure every JsonResponse data format with this."""
    return {"result": result, "error": error}
