# Generated by Django 4.1.5 on 2023-02-05 04:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0002_alter_machine_status_alter_stock_snack"),
    ]

    operations = [
        migrations.CreateModel(
            name="StockLog",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("quantity", models.PositiveIntegerField(default=0)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "machine",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="myapp.machine"
                    ),
                ),
                (
                    "snack",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="myapp.snack"
                    ),
                ),
            ],
            options={
                "ordering": ["-created"],
                "default_related_name": "stock_log",
            },
        ),
    ]