from django.contrib import admin

from ..models import Country, Region
from .country import CountryAdminModel
from .region import RegionAdminModel

admin.site.register(Region, RegionAdminModel)
admin.site.register(Country, CountryAdminModel)
