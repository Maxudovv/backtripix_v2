from django.db import models

from app.models.country import Country


class Region(models.Model):
    class STATUS:
        NOT_ACTIVE = 1
        ACTIVE = 2

        CHOICES = (
            (NOT_ACTIVE, "Не активный"),
            (ACTIVE, "Активный"),
        )

    name = models.CharField(max_length=55)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    status = models.PositiveIntegerField(
        "Статус", choices=STATUS.CHOICES, default=STATUS.NOT_ACTIVE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"
