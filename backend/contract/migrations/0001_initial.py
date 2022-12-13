# Generated by Django 4.1.3 on 2022-12-13 16:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("client", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Contract",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.FloatField(blank=True, null=True)),
                ("payment_due", models.DateField(blank=True, null=True)),
                ("status", models.BooleanField(default=False)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                (
                    "client",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contract",
                        to="client.client",
                    ),
                ),
                (
                    "sales_contact",
                    models.ForeignKey(
                        limit_choices_to={"role": "sales"},
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "contract",
                "verbose_name_plural": "contracts",
                "ordering": ["-date_created"],
            },
        ),
        migrations.CreateModel(
            name="ContractStatus",
            fields=[
                (
                    "contract",
                    models.OneToOneField(
                        limit_choices_to={"status": "True"},
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="contract.contract",
                    ),
                ),
            ],
        ),
    ]
