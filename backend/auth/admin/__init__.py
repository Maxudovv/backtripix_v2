from django.contrib import admin

from ..models import User
from .user import UserAdminModel

admin.site.register(User, UserAdminModel)
