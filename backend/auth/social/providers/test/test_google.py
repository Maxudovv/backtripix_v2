from unittest.mock import MagicMock, patch

from auth.social.providers.google import GoogleOauth
from auth.social.providers.results import ProviderResult
from common.rest_framework.testing import BaseTestCase


class GoogleOauthTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.provider = GoogleOauth()
        self.access_token = "test_token"
        self.user_id = "01234567891011121314"
        self.email = "test@example.com"
        self.mock = MagicMock()

    def test_request_url(self):
        self.provider.ACCESS_TOKEN_URL = "google.com"
        url = "google.com?id_token=test_token"
        self.assertEqual(url, self.provider.get_request_url(self.access_token))

    @patch("auth.social.providers.google.GoogleOauth.make_request")
    def test_validate_token_success__scope_is_userinfo_email(self, request_mock):
        self.mock.status_code = 200
        self.mock.json.return_value = {
            "azp": "123456788192.apps.googleusercontent.com",
            "aud": "123456788192.apps.googleusercontent.com",
            "sub": self.user_id,
            "email": self.email,
            "email_verified": "true",
            "exp": "1586845579",
        }
        request_mock.return_value = self.mock

        response = self.provider.validate_token(self.access_token)

        self.assertIsInstance(response, ProviderResult)
        self.assertEqual(response.status, ProviderResult.STATUS.SUCCESS)
        self.assertTrue(response.user_data)
        self.assertEqual(response.user_data["provider_key"], self.user_id)
        self.assertEqual(response.user_data["email"], self.email)
        self.assertIsNone(response.user_data.get("first_name", None))
        self.assertIsNone(response.error_msg)

    @patch("auth.social.providers.google.GoogleOauth.make_request")
    def test_validate_token_success__scope_is_userinfo_email__email_not_verified(
        self, request_mock
    ):
        self.mock.status_code = 200
        email_verified = "false"
        self.mock.json.return_value = {
            "azp": "123456788192.apps.googleusercontent.com",
            "aud": "123456788192.apps.googleusercontent.com",
            "sub": self.user_id,
            "email": self.email,
            "email_verified": email_verified,
            "exp": "1586845579",
        }
        request_mock.return_value = self.mock

        response = self.provider.validate_token(self.access_token)

        self.assertIsInstance(response, ProviderResult)
        self.assertEqual(response.status, ProviderResult.STATUS.SUCCESS)
        self.assertTrue(response.user_data)
        self.assertEqual(response.user_data["provider_key"], self.user_id)
        self.assertIsNone(response.user_data.get("email", None))
        self.assertIsNone(response.user_data.get("first_name", None))
        self.assertIsNone(response.error_msg)

    @patch("auth.social.providers.google.GoogleOauth.make_request")
    def test_validate_token_success__scope_is_userinfo_profile(self, request_mock):
        first_name = "First Name"
        last_name = "Last Name"
        self.mock.status_code = 200
        self.mock.json.return_value = {
            "azp": "123456788192.apps.googleusercontent.com",
            "aud": "123456788192.apps.googleusercontent.com",
            "sub": self.user_id,
            "at_hash": "hash",
            "name": "Tester",
            "picture": "https://lh5.googleusercontent.com/photo.jpg",
            "given_name": first_name,
            "family_name": last_name,
            "locale": "ru",
            "iat": "1586841246",
            "exp": "1586844846",
            "alg": "RS256",
            "kid": "6fcf413224765156bfef42fac06496a30ff5a",
            "typ": "JWT",
        }
        request_mock.return_value = self.mock

        response = self.provider.validate_token(self.access_token)

        self.assertIsInstance(response, ProviderResult)
        self.assertEqual(response.status, ProviderResult.STATUS.SUCCESS)
        self.assertTrue(response.user_data)
        self.assertEqual(response.user_data["provider_key"], self.user_id)
        self.assertIsNone(response.user_data.get("email", None))
        self.assertEqual(response.user_data["first_name"], first_name)
        self.assertEqual(response.user_data["last_name"], last_name)
        self.assertIsNone(response.error_msg)

    @patch("auth.social.providers.google.GoogleOauth.make_request")
    def test_validate_token_error_status_equals_200(self, request_mock):
        error_msg = "invalid_token"
        self.mock.status_code = 200
        self.mock.json.return_value = {
            "error": error_msg,
            "error_description": "Invalid Value",
        }
        request_mock.return_value = self.mock

        response = self.provider.validate_token(self.access_token)

        self.assertIsInstance(response, ProviderResult)
        self.assertEqual(response.status, ProviderResult.STATUS.ERROR)
        self.assertIsNone(response.user_data)
        self.assertEqual(response.error_msg, error_msg)

    @patch("auth.social.providers.google.GoogleOauth.make_request")
    def test_validate_token_error_status_not_equals_200(self, request_mock):
        self.mock.status_code = 403
        self.mock.reason_phrase = "Forbidden"
        self.mock.text = "403 Forbidden"
        request_mock.return_value = self.mock
        error_msg = "Status: 403, Reason: Forbidden, Text: 403 Forbidden"

        response = self.provider.validate_token(self.access_token)

        self.assertIsInstance(response, ProviderResult)
        self.assertEqual(response.status, ProviderResult.STATUS.ERROR)
        self.assertIsNone(response.user_data)
        self.assertEqual(response.error_msg, error_msg)

    def test_get_user_data__verified_email_exists(self):
        data = {
            "sub": self.user_id,
            "email": self.email,
            "email_verified": "true",
        }
        user_data = self.provider.get_user_data(data)
        provider_key = user_data["provider_key"]
        email = user_data["email"]
        first_name = user_data.get("first_name", None)
        last_name = user_data.get("last_name", None)

        self.assertEqual(provider_key, self.user_id)
        self.assertEqual(email, self.email)
        self.assertIsNone(first_name)
        self.assertIsNone(last_name)

    def test_get_user_data__not_verified_email_exists(self):
        data = {
            "sub": self.user_id,
            "email": self.email,
            "email_verified": "false",
        }
        user_data = self.provider.get_user_data(data)
        provider_key = user_data["provider_key"]
        email = user_data.get("email", None)
        first_name = user_data.get("first_name", None)
        last_name = user_data.get("last_name", None)

        self.assertEqual(provider_key, self.user_id)
        self.assertIsNone(email)
        self.assertIsNone(first_name)
        self.assertIsNone(last_name)

    def test_get_user_data__no_email(self):
        data = {
            "sub": self.user_id,
            "name": "Tester",
            "picture": "https://lh5.googleusercontent.com/photo.jpg",
            "given_name": "First Name",
            "family_name": "Last Name",
            "locale": "ru",
            "iat": "1123456979",
        }
        user_data = self.provider.get_user_data(data)
        provider_key = user_data["provider_key"]
        email = user_data.get("email", None)
        first_name = user_data.get("first_name", None)
        last_name = user_data.get("last_name", None)

        self.assertEqual(provider_key, self.user_id)
        self.assertIsNone(email)
        self.assertIsNotNone(first_name)
        self.assertIsNotNone(last_name)
