from django.urls import reverse
from rest_framework import status

from app.factories.region import RegionFactory
from auth.api.v0.tests.utils import user_to_dict
from auth.factories.user import UserFactory
from common.rest_framework.testing import BaseTestCase


class UserInfoTestCase(BaseTestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.jwt_authenticate(self.user)

        self.url = reverse("auth-service:api:v0:user-info")

    def test_url(self):
        self.assertEqual(self.url, "/auth-service/api/v0/user/info")

    def test_get_user_info(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_to_dict(self.user), response.data)

    def test_update_user_info(self):
        region = RegionFactory()
        response = self.client.put(
            self.url,
            data=dict(
                username="Poet",
                first_name="Alexandr",
                last_name="Pushkin",
                region_id=region.id,
                language="en",
                email="pushkin@mail.com",
            ),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Alexandr")
        self.assertEqual(self.user.last_name, "Pushkin")
        self.assertEqual(self.user.region.id, region.id)
        self.assertEqual(self.user.username, "Poet")
        self.assertEqual(self.user.email, "pushkin@mail.com")
        self.assertEqual(self.user.language, "en")
        self.assertEqual(user_to_dict(self.user), response.data)
