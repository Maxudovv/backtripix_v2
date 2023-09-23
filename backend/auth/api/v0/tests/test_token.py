from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from auth.factories.user import UserFactory
from common.rest_framework.testing import BaseTestCase


class ConnectTokenTestCase(BaseTestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url = reverse("auth-service:api:v0:token_obtain_pair")

    def test_url(self):
        self.assertEqual(self.url, "/auth-service/api/v0/connect/token/")

    def test_authenticate_by_login_and_password(self):
        password = "some-password"
        self.user.set_password(password)
        self.user.save()
        response = self.client.post(
            self.url, data=dict(username=self.user.username, password=password)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get("access_token"))
        self.assertIsNotNone(response.data.get("refresh_token"))

    def test_refresh_token(self):
        token = RefreshToken.for_user(self.user)
        response = self.client.post(self.url, data=dict(refresh_token=str(token)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get("access_token"))
        self.assertIsNotNone(response.data.get("refresh_token"))
