from django.core.validators import RegexValidator
from django.db import models


class CURRENCY(models.TextChoices):
    RUB = "RUB", "₽"
    KZT = "KZT", "₸"
    BHD = "BHD", "BHD"
    AED = "AED", "AED"
    USD = "USD", "$"
    EUR = "EUR", "€"


class Country(models.Model):
    code = models.CharField(
        "Code",
        max_length=2,
        primary_key=True,
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{2}$",
                message="Only two English uppercase letters are allowed",
            )
        ],
    )
    currency = models.CharField(max_length=3, choices=CURRENCY.choices)

    def __str__(self):
        return "Russia"

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"
