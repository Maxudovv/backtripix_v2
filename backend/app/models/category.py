from django.db import models

from common.models import LANGUAGE


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class CategoryTranslation(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="translations",
    )
    language = models.CharField(max_length=2, choices=LANGUAGE.CHOICES)
    name = models.CharField(max_length=100)
