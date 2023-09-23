from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlencode

from django.utils import translation
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from auth.models import User


@dataclass
class MockRequest:
    user: Optional[User]
    language: str


class JWTClient(APIClient):
    """APIClient with JWT authorization."""

    def jwt_authenticate(self, user: User, **kwargs):
        token = str(RefreshToken.for_user(user).access_token)
        self.credentials(HTTP_AUTHORIZATION=f"Bearer {token}", **kwargs)

    def add_credentials(self, **kwargs):
        self._credentials.update(kwargs)


class BaseTestCase(APITestCase):
    """All API Test classes should extend this class."""

    client_class = JWTClient

    def setUp(self):
        super().setUp()
        translation.activate("en")

    def add_params(self, url: str, **kwargs) -> str:
        """
        Returns url with added params.

        For example:
            add_params("/v2/projects",foo=bzz) returns "/v2/projects?foo=bzz"
        """
        return f"{url}?{urlencode(kwargs)}"

    def update_obj(self, obj, **kwargs) -> None:
        """
        Updates object with given values.

        update_obj(user, first_name="Foo", last_name="Biz")
        Is the same as code below:
            1. user.first_name = "Foo"
            2. user.last_name = "Biz"
            3. user.save(update_fields=["first_name", "last_name"]
        """
        for field, value in kwargs.items():
            setattr(obj, field, value)
        obj.save(update_fields=list(kwargs.keys()))
