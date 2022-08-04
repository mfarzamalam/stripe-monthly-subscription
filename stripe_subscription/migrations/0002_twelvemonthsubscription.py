# Generated by Django 4.1 on 2022-08-04 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stripe_subscription", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TwelveMonthSubscription",
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
                ("customer", models.CharField(max_length=256)),
                ("product", models.CharField(max_length=256)),
                ("month", models.DateTimeField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("active", "active"),
                            ("unpaid", "unpaid"),
                            ("cancelled", "cancelled"),
                        ],
                        max_length=10,
                    ),
                ),
            ],
        ),
    ]