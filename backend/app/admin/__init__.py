from django.contrib import admin

from ..models import Country, Project, Region
from ..models.category import Category
from .category import CategoryAdminModel
from .country import CountryAdminModel
from .project import ProjectAdminModel
from .region import RegionAdminModel

admin.site.register(Region, RegionAdminModel)
admin.site.register(Country, CountryAdminModel)
admin.site.register(Project, ProjectAdminModel)
admin.site.register(Category, CategoryAdminModel)
