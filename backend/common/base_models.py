from django.db import models
from django.utils.translation import ugettext_lazy as _


class ModelWithGeo(models.Model):
    lat = models.FloatField(_("Latitude"), null=True, blank=True)
    lon = models.FloatField(_("Longitude"), null=True, blank=True)

    class Meta:
        abstract = True
