# Generated by Django 4.1.5 on 2023-01-15 02:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Machine",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("location", models.TextField(max_length=500, unique=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("NORM", "Normal"), ("OUT", "Out of Stock")],
                        default="OUT",
                        max_length=10,
                    ),
                ),
            ],
            options={
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="Snack",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255, unique=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Stock",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("quantity", models.PositiveIntegerField(default=0)),
                (
                    "machine",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="myapp.machine"
                    ),
                ),
                (
                    "snack",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="myapp.snack"
                    ),
                ),
            ],
            options={
                "ordering": ["id"],
                "default_related_name": "stock",
            },
        ),
    ]
