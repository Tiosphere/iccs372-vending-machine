from django.test import TestCase, Client
from myapp.models import Machine, Stock, Snack
from myapp.serializers import (
    machine_detail_serializer,
    machine_serializer,
    snack_serializer,
    stock_serializer,
)
from django.http import HttpResponse
from django.urls import reverse
from typing import Any, Final
from django.core import management
import json


class StatusCode(enumerate):
    NORMAL = 200
    NOT_FOUND = 404
    NOT_ALLOW = 405


class TestMachineView(TestCase):
    def setUpTestData():
        management.call_command("create_sample")

    def setUp(self):
        self.client: Client = Client()
        self.url: str = reverse("myapp:machine")

    def test_get_simple(self):
        response: HttpResponse = self.client.get(self.url)
        content: dict[str, Any] = json.loads(response.content)
        result: list[dict[str, Any]] = content.get("result")
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertEqual(len(result), 20)
        for item in result:
            self.assertEqual(len(item.get("stock", [])), 0)

    def test_get_options_detail(self):
        # test detail=true
        response: HttpResponse = self.client.get(self.url + "?detail=true")
        content: dict[str, Any] = json.loads(response.content)
        result: list[dict[str, Any]] = content.get("result")
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertEqual(len(result), 20)
        for item in result:
            instance = Machine.objects.get(id=item.get("id"))
            self.assertEqual(
                len(item.get("stock", [])), Stock.objects.filter(machine=instance).count()
            )

        # Test detail=false
        response: HttpResponse = self.client.get(self.url + "?detail=false")
        content: dict[str, Any] = json.loads(response.content)
        result: list[dict[str, Any]] = content.get("result")
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertEqual(len(result), 20)
        for item in result:
            self.assertEqual(len(item.get("stock", [])), 0)

    def test_get_options_name(self):
        # empty fields
        response: HttpResponse = self.client.get(self.url + "?name=")
        content: dict[str, Any] = json.loads(response.content)
        result: list[dict[str, Any]] = content.get("result")
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertEqual(len(result), 20)
        # search something
        response: HttpResponse = self.client.get(self.url + "?name=science")
        content: dict[str, Any] = json.loads(response.content)
        result: list[dict[str, Any]] = content.get("result")
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertEqual(len(result), 10)
        for item in result:
            self.assertIn("Building", item.get("name"))
        # search partial
        response: HttpResponse = self.client.get(self.url + "?name=scien")
        content: dict[str, Any] = json.loads(response.content)
        result: list[dict[str, Any]] = content.get("result")
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertEqual(len(result), 10)
        for item in result:
            self.assertIn("Building", item.get("name"))

    def test_get_options_location(self):
        # empty fields
        response: HttpResponse = self.client.get(self.url + "?location=")
        content: dict[str, Any] = json.loads(response.content)
        result: list[dict[str, Any]] = content.get("result")
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertEqual(len(result), 20)
        # search something
        response: HttpResponse = self.client.get(self.url + "?location=science")
        content: dict[str, Any] = json.loads(response.content)
        result: list[dict[str, Any]] = content.get("result")
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertEqual(len(result), 10)
        for item in result:
            self.assertIn("Building", item.get("name"))
        # search partial
        response: HttpResponse = self.client.get(self.url + "?location=scien")
        content: dict[str, Any] = json.loads(response.content)
        result: list[dict[str, Any]] = content.get("result")
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertEqual(len(result), 10)
        for item in result:
            self.assertIn("Building", item.get("name"))

    def test_post_simple(self):
        response: HttpResponse = self.client.post(
            self.url, data={"name": "new machine", "location": "new machine location"}
        )
        content: dict[str, Any] = json.loads(response.content)
        result: dict[str, Any] = content.get("result")
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertEqual(result, machine_serializer(Machine.objects.last()))
        # self.assertEqual(result.get("name"), "new machine")
        # self.assertEqual(result.get("location"), "new machine location")
        # self.assertEqual(result.get("status"), Machine.MachineStatus.OFFLINE)

    def test_delete_simple(self):
        response: HttpResponse = self.client.delete(self.url)
        self.assertEqual(response.status_code, StatusCode.NOT_ALLOW)

    def test_put_simple(self):
        response: HttpResponse = self.client.put(self.url)
        self.assertEqual(response.status_code, StatusCode.NOT_ALLOW)


class TestMachineInstance(TestCase):
    def setUpTestData():
        management.call_command("create_sample")

    def setUp(self):
        self.client: Client = Client()
        self.id: int = 1
        self.url: str = reverse("myapp:machine_instance", args=[self.id])

    def test_invalid_id(self):
        response: HttpResponse = self.client.get(
            reverse("myapp:machine_instance", args=[100])
        )
        content: dict[str, Any] = json.loads(response.content)
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertEqual(content.get("error"), True)

    def test_get_simple(self):
        response: HttpResponse = self.client.get(self.url)
        content: dict[str, Any] = json.loads(response.content)
        result: dict[str, Any] = content.get("result")
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertEqual(
            result, machine_detail_serializer(Machine.objects.get(id=self.id))
        )

    def test_post_simple(self):
        response: HttpResponse = self.client.post(
            self.url, data={"name": "new machine", "location": "new machine location"}
        )
        content: dict[str, Any] = json.loads(response.content)
        result: list[dict[str, Any]] = content.get("result")
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertEqual(result, machine_serializer(Machine.objects.first()))

    def test_delete_simple(self):
        response: HttpResponse = self.client.delete(self.url)
        self.assertEqual(response.status_code, StatusCode.NOT_ALLOW)

    def test_put_simple(self):
        response: HttpResponse = self.client.put(self.url)
        self.assertEqual(response.status_code, StatusCode.NOT_ALLOW)

    def test_get_options_delete(self):
        response: HttpResponse = self.client.get(self.url + "?delete=True")
        content: dict[str, Any] = json.loads(response.content)
        result: dict[str, Any] = content.get("result")
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertIsNone(Machine.objects.filter(id=self.id).first())


class TestSnackView(TestCase):
    def setUpTestData():
        management.call_command("create_sample")

    def setUp(self):
        self.client: Client = Client()
        self.url: str = reverse("myapp:snack")

    def test_get_simple(self):
        response: HttpResponse = self.client.get(self.url)
        content: dict[str, Any] = json.loads(response.content)
        result: list[dict[str, Any]] = content.get("result")
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertEqual(len(result), Snack.objects.all().count())

    def test_get_options_name(self):
        # empty fields
        response: HttpResponse = self.client.get(self.url + "?name=")
        content: dict[str, Any] = json.loads(response.content)
        result: list[dict[str, Any]] = content.get("result")
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertEqual(len(result), Snack.objects.all().count())
        # search something
        response: HttpResponse = self.client.get(self.url + "?name=water")
        content: dict[str, Any] = json.loads(response.content)
        result: list[dict[str, Any]] = content.get("result")
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertEqual(
            len(result), Snack.objects.filter(name__icontains="water").count()
        )

    def test_post_simple(self):
        response: HttpResponse = self.client.post(self.url, data={"name": "new snack"})
        content: dict[str, Any] = json.loads(response.content)
        result: dict[str, Any] = content.get("result")
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertEqual(result, snack_serializer(Snack.objects.last()))

    def test_delete_simple(self):
        response: HttpResponse = self.client.delete(self.url)
        self.assertEqual(response.status_code, StatusCode.NOT_ALLOW)

    def test_put_simple(self):
        response: HttpResponse = self.client.put(self.url)
        self.assertEqual(response.status_code, StatusCode.NOT_ALLOW)


class TestSnackInstance(TestCase):
    def setUpTestData():
        management.call_command("create_sample")

    def setUp(self):
        self.client: Client = Client()
        self.id: int = 1
        self.url: str = reverse("myapp:snack_instance", args=[self.id])

    def test_invalid_id(self):
        response: HttpResponse = self.client.get(
            reverse("myapp:snack_instance", args=[100])
        )
        content: dict[str, Any] = json.loads(response.content)
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertEqual(content.get("error"), True)

    def test_get_simple(self):
        response: HttpResponse = self.client.get(self.url)
        content: dict[str, Any] = json.loads(response.content)
        result: dict[str, Any] = content.get("result")
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertEqual(result, snack_serializer(Snack.objects.get(id=self.id)))

    def test_post_simple(self):
        response: HttpResponse = self.client.post(
            self.url, data={"name": "new snack name"}
        )
        content: dict[str, Any] = json.loads(response.content)
        result: list[dict[str, Any]] = content.get("result")
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertEqual(result, snack_serializer(Snack.objects.get(id=self.id)))

    def test_delete_simple(self):
        response: HttpResponse = self.client.delete(self.url)
        self.assertEqual(response.status_code, StatusCode.NOT_ALLOW)

    def test_put_simple(self):
        response: HttpResponse = self.client.put(self.url)
        self.assertEqual(response.status_code, StatusCode.NOT_ALLOW)

    def test_get_options_delete(self):
        response: HttpResponse = self.client.get(self.url + "?delete=True")
        content: dict[str, Any] = json.loads(response.content)
        result: dict[str, Any] = content.get("result")
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertIsNone(Snack.objects.filter(id=self.id).first())


class TestStockInstance(TestCase):
    def setUpTestData():
        management.call_command("create_sample")

    def setUp(self):
        self.client: Client = Client()
        self.machine_id: int = 1
        self.machine_instance = Machine.objects.get(id=self.machine_id)
        self.snack_id = self.machine_instance.stock.first().snack.id
        self.url: str = reverse("myapp:stock", args=[self.machine_id, self.snack_id])

    def test_get_simple(self):
        response: HttpResponse = self.client.get(self.url)
        content: dict[str, Any] = json.loads(response.content)
        result: dict[str, Any] = content.get("result")
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertEqual(result, machine_detail_serializer(self.machine_instance))

    def test_get_options_add(self):
        response: HttpResponse = self.client.get(self.url + "?add=20")
        content: dict[str, Any] = json.loads(response.content)
        result: dict[str, Any] = content.get("result")
        self.machine_instance.refresh_from_db()
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertEqual(result, machine_detail_serializer(self.machine_instance))

    def test_get_options_minus(self):
        response: HttpResponse = self.client.get(self.url + "?minus=20")
        content: dict[str, Any] = json.loads(response.content)
        result: dict[str, Any] = content.get("result")
        self.machine_instance.refresh_from_db()
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertEqual(result, machine_detail_serializer(self.machine_instance))

    def test_get_options_set(self):
        response: HttpResponse = self.client.get(self.url + "?set=200")
        content: dict[str, Any] = json.loads(response.content)
        result: dict[str, Any] = content.get("result")
        self.machine_instance.refresh_from_db()
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertEqual(result, machine_detail_serializer(self.machine_instance))

    def test_get_options_error(self):
        # as negative integer
        response: HttpResponse = self.client.get(self.url + "?set=-300")
        content: dict[str, Any] = json.loads(response.content)
        result: dict[str, Any] = content.get("result")
        self.machine_instance.refresh_from_db()
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertEqual(content.get("error"), True)
        # as text
        response: HttpResponse = self.client.get(self.url + "?set=hej")
        content: dict[str, Any] = json.loads(response.content)
        result: dict[str, Any] = content.get("result")
        self.machine_instance.refresh_from_db()
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertEqual(content.get("error"), True)

    def test_get_error_id(self):
        # machine id error
        response: HttpResponse = self.client.get(
            reverse("myapp:stock", args=[100, self.snack_id])
        )
        content: dict[str, Any] = json.loads(response.content)
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertEqual(content.get("error"), True)
        # snack id error
        response: HttpResponse = self.client.get(
            reverse("myapp:stock", args=[self.machine_id, 100])
        )
        content: dict[str, Any] = json.loads(response.content)
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertEqual(content.get("error"), True)

    def test_post_simple(self):
        response: HttpResponse = self.client.post(self.url)
        self.assertEqual(response.status_code, StatusCode.NOT_ALLOW)

    def test_delete_simple(self):
        response: HttpResponse = self.client.delete(self.url)
        self.assertEqual(response.status_code, StatusCode.NOT_ALLOW)

    def test_put_simple(self):
        response: HttpResponse = self.client.put(self.url)
        self.assertEqual(response.status_code, StatusCode.NOT_ALLOW)

    def test_get_options_delete(self):
        response: HttpResponse = self.client.get(self.url + "?delete=True")
        content: dict[str, Any] = json.loads(response.content)
        self.assertEqual(response.status_code, StatusCode.NORMAL)
        self.assertEqual(
            0,
            Machine.objects.get(id=self.machine_id)
            .stock.filter(snack=Snack.objects.get(id=self.snack_id))
            .count(),
        )
