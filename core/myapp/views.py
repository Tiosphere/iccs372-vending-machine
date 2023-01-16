from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotAllowed,
    JsonResponse,
)
from django.db.models.manager import BaseManager
from myapp.forms import MachineForm, SnackForm, StockForm
from myapp.models import Machine, Snack, Stock
from myapp.serializers import (
    json_format,
    machine_detail_serializer,
    machine_serializer,
    snack_serializer,
)


# Create your views here.
def machine_views(request: HttpRequest) -> HttpResponse:
    """
    method POST:
        to create new machine and return new created machine
    method GET:
        return list of machine
    options:
        detail: boolean = False (default) if True return list of machine with stock detail

        name: string to search for machine that contain specific name

        location: string to search for machine that contain specific location
    """
    if request.method == "POST":
        form = MachineForm(request.POST)
        if form.is_valid():
            return JsonResponse(data=json_format(machine_serializer(form.save(True))))
        else:
            return JsonResponse(data=json_format(form.errors.get_json_data, error=True))

    elif request.method == "GET":
        query: BaseManager[Machine] = Machine.objects.all()
        # filter process
        if request.GET.get("name") is not None:
            query = query.filter(name__icontains=request.GET.get("name"))
        if request.GET.get("location") is not None:
            query = query.filter(location__icontains=request.GET.get("location"))
        # Check for detail arg
        if not request.GET.get("detail", False):
            return JsonResponse(
                data=json_format([machine_serializer(item) for item in query]),
            )
        else:
            return JsonResponse(
                data=json_format(
                    [
                        machine_detail_serializer(item)
                        for item in query.prefetch_related("stock")
                    ]
                ),
            )
    return HttpResponseNotAllowed(["GET", "POST"])


def machine_instance(request: HttpRequest, id: int) -> HttpResponse:
    """
    method POST:
        to update data of current machine and return new update machine instance
    method GET:
        return data of current machine
        options:
            delete: boolean if True delete machine with this id
    """
    # check if instance exist or not
    instance = Machine.objects.filter(id=id).first()
    if instance is None:
        return JsonResponse(
            data=json_format("Can't find machine with this id", error=True)
        )
    if request.method == "POST":
        # check form
        form = MachineForm(request.POST, instance=instance)
        if form.is_valid():
            instance: Machine = form.save(commit=False)
            return JsonResponse(data=json_format(machine_serializer(form.save(True))))
        else:
            return JsonResponse(data=json_format(form.errors.get_json_data(), error=True))
    elif request.method == "GET":
        # check delete arg
        if request.GET.get("delete", False):
            instance.delete()
            return JsonResponse(data=json_format(f"Successfully deleted machine id={id}"))
        return JsonResponse(data=json_format(machine_detail_serializer(instance)))

    return HttpResponseNotAllowed(["GET", "POST"])


def snack_views(request: HttpRequest) -> JsonResponse:
    """
    method POST:
        to create new snack and return new created snack
    method GET:
        return list of snack
    """
    if request.method == "POST":
        form = SnackForm(request.POST)
        if form.is_valid():
            return JsonResponse(data=json_format(snack_serializer(form.save(True))))
        else:
            return JsonResponse(data=json_format(form.errors.get_json_data, error=True))
    elif request.method == "GET":
        return JsonResponse(
            data=json_format([snack_serializer(item) for item in Snack.objects.all()])
        )
    return HttpResponseNotAllowed(["GET", "POST"])


def snack_instance(request: HttpRequest, id: int) -> HttpResponse:
    """
    method POST:
        to update data of current snack and return new update snack instance
    method GET:
        return data of current snack
        options:
            delete: boolean if True delete snack with this id
    """
    # check if instance exist or not
    instance = Snack.objects.filter(id=id).first()
    if instance is None:
        return JsonResponse(data=json_format("Can't find snack with this id", error=True))
    if request.method == "POST":
        # check form
        form = SnackForm(request.POST, instance=instance)
        if form.is_valid():
            instance: Snack = form.save(commit=False)
            return JsonResponse(data=json_format(snack_serializer(form.save(True))))
        else:
            return JsonResponse(data=json_format(form.errors.get_json_data(), error=True))
    elif request.method == "GET":
        # check delete arg
        if request.GET.get("delete", False):
            instance.delete()
            return JsonResponse(data=json_format(f"Successfully deleted snack id={id}"))
        return JsonResponse(data=json_format(snack_serializer(instance)))

    return HttpResponseNotAllowed(["GET", "POST"])


def stock_view(request: HttpRequest, machine_id: int, snack_id: int) -> HttpResponse:
    """
    method GET:
        return data of current of machine
        if current machine didn't has this snack.
        It will be auto add with quantity 0 as default.
            options:
                delete: boolean if True remove snack from machine
                add: positive integer amount of snack will be add
                minus: positive integer amount of snack will be minus


    """
    # check if machine_id valid
    machine_instance = Machine.objects.filter(id=machine_id).first()
    if machine_instance is None:
        return JsonResponse(
            data=json_format("Can't find machine with this id", error=True)
        )
    # check if snack_id valid
    snack_instance = Snack.objects.filter(id=snack_id).first()
    if snack_instance is None:
        return JsonResponse(data=json_format("Can't find snack with this id", error=True))
    instance = Stock.objects.get_or_create(
        machine=machine_instance, snack=snack_instance
    )[0]
    if request.method == "GET":
        if request.GET.get("delete", False):
            instance.delete()
            return JsonResponse(
                data=json_format(
                    f"remove snack {snack_instance.name} from machine id={machine_instance.id}"
                )
            )
        add: str = request.GET.get("add", "0")
        minus: str = request.GET.get("minus", "0")
        start: str = request.GET.get("set", str(instance.quantity))
        if not (add.isnumeric() and minus.isnumeric() and start.isnumeric()):
            return JsonResponse(
                data=json_format("Invalid parameter(s) is found", error=True)
            )
        instance.quantity = abs(int(start)) + abs(int(add)) - abs(int(minus))
        instance.save()
        return JsonResponse(
            data=json_format(
                machine_detail_serializer(Machine.objects.get(id=machine_id))
            )
        )
    return HttpResponseNotAllowed(["GET"])
