import importlib
import logging
from typing import Any, Dict, List, Optional
from uuid import uuid4

from django.conf import settings
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response

from auth.models import User
from auth.social.providers.base import BaseAuth
from auth.social.providers.results import ProviderResult

logger = logging.getLogger(__name__)


class SocialUserTokenObtainPair:
    """The main class that manages social users token obtaining."""

    def __init__(self, request_data: Dict[str, Any]):
        self.data = request_data

    def _check_provider_settings(self) -> Optional[Response]:
        login_provider = self.data["login_provider"]
        if not settings.SOCIAL_PROVIDERS:
            raise ValueError("SOCIAL_PROVIDERS setting is not set")
        if login_provider not in settings.SOCIAL_PROVIDERS:
            return Response(
                {
                    "code": "405",
                    "message": f"Login provider {login_provider} is not supported",
                    "errors": [],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return None

    def _get_provider(self, login_provider: str) -> BaseAuth:
        """Get provider class appropriate to login provider"""
        module_name, class_name = settings.SOCIAL_PROVIDERS[login_provider].rsplit(
            ".", 1
        )
        return getattr(importlib.import_module(module_name), class_name)()

    def get_email_user(self, email: str) -> Optional[User]:
        """Try to get a user with an email obtained from social data"""
        return User.objects.filter(
            Q(username__exact=email) | Q(email__exact=email)
        ).first()

    def get_social_user(self, login_provider: str, provider_key: str) -> Optional[User]:
        """Get a social user if already exists"""
        return User.objects.filter(
            login_provider=login_provider, provider_key=provider_key
        ).first()

    def validate_social_access_token(self) -> ProviderResult:
        return self.provider.validate_token(self.data["access_token"])

    def handle(self) -> Response:
        login_provider = self.data["login_provider"]
        # Check login_provider exists in SOCIAL_PROVIDERS settings.
        _provider_settings_error = self._check_provider_settings()
        # If login_provider not set in settings return the error.
        if _provider_settings_error:
            return _provider_settings_error
        # Get the right provider.
        self.provider = self._get_provider(login_provider)
        # Check the corresponding social network token.
        provider_result = self.validate_social_access_token()

        if not provider_result.ok():
            return Response(
                {
                    "code": "401",
                    "message": provider_result.error_msg,
                    "errors": [],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        assert isinstance(provider_result.user_data, dict)
        provider_key = provider_result.user_data["provider_key"]

        social_user = self.get_social_user(
            login_provider=login_provider,
            provider_key=provider_key,
        )

        if not social_user:
            # No users exist. Create a new social user.
            social_user = self.create_new_social_user()
            logger.info(f"New social user - <{social_user}> has created.")
        # Update social data of the user.
        assert isinstance(social_user, User)
        social_user = self.update_user_social_data(
            social_user, login_provider, provider_key, provider_result.user_data
        )
        # Get a new token.
        token_data = social_user.get_tokens()

        return Response(token_data, status=status.HTTP_200_OK)

    def create_new_social_user(self) -> User:
        return User.objects.create_user(username=str(uuid4()))

    def update_user_social_data(
        self,
        user: User,
        login_provider: str,
        provider_key: str,
        user_data: Dict[str, Any],
    ) -> User:
        fields_to_update: List[str] = []
        email = user_data.get("email", None)
        first_name = user_data.get("first_name", None)
        last_name = user_data.get("last_name", None)
        if not all((user.login_provider, user.provider_key)):
            user.login_provider = login_provider
            user.provider_key = provider_key
            fields_to_update = ["login_provider", "provider_key"]
        if email:
            user.email = email
            user.is_registered = True
            fields_to_update.append("email")
            fields_to_update.append("is_registered")
        if first_name and last_name and not all((user.first_name, user.last_name)):
            user.first_name = first_name
            user.last_name = last_name
            fields_to_update.extend(["first_name", "last_name"])
        if fields_to_update:
            user.save(update_fields=fields_to_update)

        return user
