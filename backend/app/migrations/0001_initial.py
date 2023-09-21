# Generated by Django 4.2.5 on 2023-09-21 09:38
from typing import List

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies: List = []

    operations = [
        migrations.CreateModel(
            name="Country",
            fields=[
                (
                    "code",
                    models.CharField(
                        max_length=2,
                        primary_key=True,
                        serialize=False,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Only two English uppercase letters are allowed",
                                regex="^[A-Z]{2}$",
                            )
                        ],
                        verbose_name="Code",
                    ),
                ),
                (
                    "currency",
                    models.CharField(
                        choices=[
                            ("RUB", "₽"),
                            ("KZT", "₸"),
                            ("BHD", "BHD"),
                            ("AED", "AED"),
                            ("USD", "$"),
                            ("EUR", "€"),
                        ],
                        max_length=3,
                    ),
                ),
            ],
            options={
                "verbose_name": "Страна",
                "verbose_name_plural": "Страны",
            },
        ),
        migrations.CreateModel(
            name="Region",
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
                ("name", models.CharField(max_length=55)),
                (
                    "status",
                    models.PositiveIntegerField(
                        choices=[(1, "Не активный"), (2, "Активный")],
                        default=1,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="app.country"
                    ),
                ),
            ],
            options={
                "verbose_name": "Регион",
                "verbose_name_plural": "Регионы",
            },
        ),
    ]
