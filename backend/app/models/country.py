from django.core.validators import RegexValidator
from django.db import models


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

    def __str__(self):
        return self.code

    class Meta:
        verbose_name_plural = "Countries"
