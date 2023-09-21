from datetime import datetime, timedelta
from typing import Any, Dict

import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField, ProcessedImageField
from pilkit.processors import SmartResize
from rest_framework_simplejwt.tokens import RefreshToken

from app.models.region import Region
from app.utils import upload_to
from common.models import LANGUAGE


class User(AbstractUser):
    class PROVIDER:
        GOOGLE = "google"
        ANONYM = "anonymous"
        NONE = ""

        CHOICES = (
            (GOOGLE, _("Google")),
            (ANONYM, _("Anonymous")),
            (NONE, "-"),
        )

    username = models.CharField(
        db_index=True,
        max_length=255,
        unique=True,
        blank=False,
        null=False,
        verbose_name="Username",
    )
    email = models.EmailField(
        validators=[validators.validate_email],
        blank=True,
        verbose_name="Электронная почта",
    )
    language = models.CharField(
        _("Language"), max_length=2, choices=LANGUAGE.CHOICES, default=LANGUAGE.RU
    )

    region = models.ForeignKey(
        Region, on_delete=models.SET_NULL, null=True, verbose_name="Регион"
    )
    original_avatar = ProcessedImageField(
        upload_to=upload_to,
        format="JPEG",
        null=True,
        blank=True,
    )
    small_avatar = ImageSpecField(
        source="original_avatar",
        processors=[SmartResize(width=48, height=48, upscale=True)],
        format="JPEG",
    )

    avatar128 = ImageSpecField(
        source="original_avatar",
        processors=[SmartResize(width=128, height=128, upscale=True)],
        format="JPEG",
    )

    login_provider = models.CharField(
        _("Login Provider"),
        max_length=20,
        default=PROVIDER.NONE,
        choices=PROVIDER.CHOICES,
        blank=True,
    )
    provider_key = models.CharField(
        _("Provider Key"), max_length=100, default="", blank=True
    )

    USERNAME_FIELD = "username"

    def __str__(self):
        return f"{self.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_tokens(self) -> Dict[str, Any]:
        refresh = RefreshToken.for_user(self)
        return {
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token),
        }

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Создает веб-токен JSON, в котором хранится идентификатор
        этого пользователя и срок его действия
        составляет 60 дней в будущем.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode(
            {"id": self.pk, "exp": int(dt.strftime("%s"))},
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        return token
