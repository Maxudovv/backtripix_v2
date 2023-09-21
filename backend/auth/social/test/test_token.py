from unittest.mock import MagicMock, Mock, patch
from uuid import uuid4

from django.contrib.auth.hashers import check_password
from django.test import override_settings

from auth.factories.user import UserFactory
from auth.models import User
from auth.social.providers.results import ProviderResult
from auth.social.token import SocialUserTokenObtainPair
from common.rest_framework.testing import BaseTestCase


@override_settings(SOCIAL_PROVIDERS={"social": "auth.social.providers.social"})
@patch("auth.social.token.SocialUserTokenObtainPair._get_provider", Mock())
@patch("auth.social.token.SocialUserTokenObtainPair.validate_social_access_token")
class SocialUserTokenObtainPairTestCase(BaseTestCase):
    fixtures = ("countries.yaml",)

    def setUp(self):
        super().setUp()
        self.social_data = {"access_token": "social_token", "login_provider": "social"}
        self.data = {
            "username": str(uuid4()),
            "password": str(uuid4()),
            **self.social_data,
        }
        self.email_user_password = "122122"

        self.mock = MagicMock()
        self.mock.user_data = {"provider_key": "123456"}
        self.mock.status = ProviderResult.STATUS.SUCCESS

        self.response_email_data = {"email": "test@example.com"}
        self.response_user_names = {"first_name": "Alex", "last_name": "Pushkin"}

    def assert_token(self, response):
        """Validate JWT token response."""
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["access_token"])
        self.assertTrue(response.data["refresh_token"])
        self.assertEqual(response.data["token_type"], "Bearer")
        self.assertTrue(response.data["expires_in"])
        self.assertTrue(response.data["id_token"])

    def test_social_data_new_user_created(self, validate_token_mock):
        validate_token_mock.return_value = self.mock
        # Obtain a token pair.
        response = SocialUserTokenObtainPair(self.social_data).handle()

        # Validate result.
        self.assert_token(response)
        # Make sure that a new user was created.
        user = User.objects.get(login_provider=self.social_data["login_provider"])
        self.assertEqual(user.provider_key, self.mock.user_data["provider_key"])

    def test_social_data_social_user_exists(self, validate_token_mock):
        social_user = UserFactory(
            login_provider=self.social_data["login_provider"],
            provider_key=self.mock.user_data["provider_key"],
        )
        validate_token_mock.return_value = self.mock
        # Obtain a token pair.
        response = SocialUserTokenObtainPair(self.social_data).handle()

        # Validate result.
        self.assert_token(response)
        # Make sure that no new user was created.
        user = User.objects.get(login_provider=self.social_data["login_provider"])
        self.assertEqual(user.provider_key, self.mock.user_data["provider_key"])
        self.assertEqual(user, social_user)

    def test_social_data_email_user_exists_username(self, validate_token_mock):
        # Add an email to the provider result.
        self.mock.user_data.update(self.response_email_data)
        email_user = UserFactory(
            username=self.response_email_data["email"],
            password=self.email_user_password,
        )
        validate_token_mock.return_value = self.mock
        # Obtain a token pair.
        response = SocialUserTokenObtainPair(self.social_data).handle()

        # Validate result.
        self.assert_token(response)
        # Make sure that no new user was created.
        user = User.objects.get(login_provider=self.social_data["login_provider"])
        self.assertEqual(user.provider_key, self.mock.user_data["provider_key"])
        self.assertEqual(user, email_user)
        # Make sure that a user can log in with his own password.
        self.assertTrue(check_password(self.email_user_password, user.password))
        self.assertTrue(user.has_usable_password())

    def test_social_data_email_user_exists_email(self, validate_token_mock):
        # Add an email to the provider result.
        self.mock.user_data.update(self.response_email_data)
        email_user = UserFactory(
            email=self.response_email_data["email"], password=self.email_user_password
        )
        validate_token_mock.return_value = self.mock
        # Obtain a token pair.
        response = SocialUserTokenObtainPair(self.social_data).handle()

        # Validate result.
        self.assert_token(response)
        # Make sure that no new user was created.
        user = User.objects.get(login_provider=self.social_data["login_provider"])
        self.assertEqual(user.provider_key, self.mock.user_data["provider_key"])
        self.assertEqual(user, email_user)
        # Make sure that a user can log in with his own password.
        self.assertTrue(check_password(self.email_user_password, user.password))
        self.assertTrue(user.has_usable_password())

    def test_social_data_email_user_exists_email_case_insensitive(
        self, validate_token_mock
    ):
        # Add an email to the provider result.
        self.mock.user_data.update(self.response_email_data)
        email_user = UserFactory(
            email=self.response_email_data["email"].upper(),
            password=self.email_user_password,
        )
        validate_token_mock.return_value = self.mock
        # Obtain a token pair.
        response = SocialUserTokenObtainPair(self.social_data).handle()

        # Validate result.
        self.assert_token(response)
        # Make sure that no new user was created.
        user = User.objects.get(login_provider=self.social_data["login_provider"])
        self.assertEqual(user.provider_key, self.mock.user_data["provider_key"])
        self.assertEqual(user, email_user)
        # Make sure that a user can log in with his own password.
        self.assertTrue(check_password(self.email_user_password, user.password))
        self.assertTrue(user.has_usable_password())

    def test_data_temp_user_exists(self, validate_token_mock):
        temp_user = UserFactory(
            username=self.data["username"], password=self.data["password"]
        )
        validate_token_mock.return_value = self.mock
        # Obtain a token pair.
        response = SocialUserTokenObtainPair(self.data).handle()

        # Validate result.
        self.assert_token(response)
        # Make sure that no new user was created.
        user = User.objects.get(login_provider=self.data["login_provider"])
        self.assertEqual(user.provider_key, self.mock.user_data["provider_key"])
        self.assertEqual(user, temp_user)
        # Make sure that a temp user no longer can't log in using his own password.
        self.assertFalse(check_password(self.data["password"], user.password))
        self.assertFalse(user.has_usable_password())

    def test_data_temp_user_and_email_user_exist(self, validate_token_mock):
        UserFactory(username=self.data["username"], password=self.data["password"])
        # Add an email to the provider result.
        self.mock.user_data.update(self.response_email_data)
        email_user = UserFactory(
            email=self.response_email_data["email"], password=self.email_user_password
        )
        validate_token_mock.return_value = self.mock
        # Obtain a token pair.
        response = SocialUserTokenObtainPair(self.data).handle()

        # Validate result.
        self.assert_token(response)
        # Make sure that users were merged.
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(login_provider=self.data["login_provider"])
        self.assertEqual(user.provider_key, self.mock.user_data["provider_key"])
        self.assertEqual(user, email_user)
        # Make sure that a user can log in with his own password.
        self.assertTrue(check_password(self.email_user_password, user.password))
        self.assertTrue(user.has_usable_password())

    def test_data_temp_user_and_email_user_are_the_same(self, validate_token_mock):
        temp_user = UserFactory(
            username=self.data["username"],
            password=self.data["password"],
            email=self.response_email_data["email"],
        )
        # Add an email to the provider result.
        self.mock.user_data.update(self.response_email_data)
        validate_token_mock.return_value = self.mock
        # Obtain a token pair.
        response = SocialUserTokenObtainPair(self.data).handle()

        # Validate result.
        self.assert_token(response)
        # Make sure that no new user was created.
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(login_provider=self.data["login_provider"])
        self.assertEqual(user.provider_key, self.mock.user_data["provider_key"])
        self.assertEqual(user, temp_user)
        # Make sure that a user can log in with his own password.
        self.assertTrue(check_password(self.data["password"], user.password))
        self.assertTrue(user.has_usable_password())

    def test_data_temp_user_and_social_user_exist(self, validate_token_mock):
        UserFactory(username=self.data["username"], password=self.data["password"])
        social_user = UserFactory(
            login_provider=self.social_data["login_provider"],
            provider_key=self.mock.user_data["provider_key"],
        )
        # UserFactory add a password so make it unusable.
        social_user.set_unusable_password()
        social_user.save()
        validate_token_mock.return_value = self.mock
        # Obtain a token pair.
        response = SocialUserTokenObtainPair(self.data).handle()

        # Validate result.
        self.assert_token(response)
        # Make sure that users were merged.
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(login_provider=self.data["login_provider"])
        self.assertEqual(user.provider_key, self.mock.user_data["provider_key"])
        self.assertEqual(user, social_user)
        # Make sure that a user no longer can't log in using his own password.
        self.assertFalse(check_password(self.data["password"], user.password))
        self.assertFalse(user.has_usable_password())

    def test_data_temp_user_and_social_user_are_the_same(self, validate_token_mock):
        temp_user = UserFactory(
            username=self.data["username"],
            password=self.data["password"],
            login_provider=self.social_data["login_provider"],
            provider_key=self.mock.user_data["provider_key"],
        )
        # Add an email to the provider result.
        self.mock.user_data.update(self.response_email_data)
        validate_token_mock.return_value = self.mock
        # Obtain a token pair.
        response = SocialUserTokenObtainPair(self.data).handle()

        # Validate result.
        self.assert_token(response)
        # Make sure that no new user was created.
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(login_provider=self.data["login_provider"])
        self.assertEqual(user.provider_key, self.mock.user_data["provider_key"])
        self.assertEqual(user, temp_user)
        # The user can log in with his own password because we didn't make it unusable.
        self.assertTrue(check_password(self.data["password"], user.password))
        self.assertTrue(user.has_usable_password())

    def test_data_email_user_and_social_user_exist(self, validate_token_mock):
        # Add an email to the provider result.
        self.mock.user_data.update(self.response_email_data)
        email_user = UserFactory(
            email=self.response_email_data["email"], password=self.email_user_password
        )
        UserFactory(
            login_provider=self.social_data["login_provider"],
            provider_key=self.mock.user_data["provider_key"],
        )
        validate_token_mock.return_value = self.mock
        # Obtain a token pair.
        response = SocialUserTokenObtainPair(self.data).handle()

        # Validate result.
        self.assert_token(response)
        # Make sure that users were merged.
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(login_provider=self.data["login_provider"])
        self.assertEqual(user.provider_key, self.mock.user_data["provider_key"])
        self.assertEqual(user, email_user)
        # Make sure that a user can log in with his own password.
        self.assertTrue(check_password(self.email_user_password, user.password))
        self.assertTrue(user.has_usable_password())

    def test_data_email_user_and_social_user_are_the_same(self, validate_token_mock):
        # Add an email to the provider result.
        self.mock.user_data.update(self.response_email_data)
        email_user = UserFactory(
            email=self.response_email_data["email"],
            password=self.email_user_password,
            login_provider=self.social_data["login_provider"],
            provider_key=self.mock.user_data["provider_key"],
        )
        validate_token_mock.return_value = self.mock
        # Obtain a token pair.
        response = SocialUserTokenObtainPair(self.data).handle()

        # Validate result.
        self.assert_token(response)
        # Make sure that no new user created.
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(login_provider=self.data["login_provider"])
        self.assertEqual(user.provider_key, self.mock.user_data["provider_key"])
        self.assertEqual(user, email_user)
        # Make sure that a user can log in with his own password.
        self.assertTrue(check_password(self.email_user_password, user.password))
        self.assertTrue(user.has_usable_password())

    def test_data_temp_user_email_user_and_social_user_exist(self, validate_token_mock):
        UserFactory(username=self.data["username"], password=self.data["password"])
        # Add an email to the provider result.
        self.mock.user_data.update(self.response_email_data)
        email_user = UserFactory(
            email=self.response_email_data["email"], password=self.email_user_password
        )
        UserFactory(
            login_provider=self.social_data["login_provider"],
            provider_key=self.mock.user_data["provider_key"],
        )
        validate_token_mock.return_value = self.mock
        # Obtain a token pair.
        response = SocialUserTokenObtainPair(self.data).handle()

        # Validate result.
        self.assert_token(response)
        # Make sure that users were merged.
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(login_provider=self.data["login_provider"])
        self.assertEqual(user.provider_key, self.mock.user_data["provider_key"])
        self.assertEqual(user, email_user)
        # Make sure that a user can log in with his own password.
        self.assertTrue(check_password(self.email_user_password, user.password))
        self.assertTrue(user.has_usable_password())

    def test_data_temp_user_email_user_and_social_user_are_the_same(
        self, validate_token_mock
    ):
        temp_user = UserFactory(
            username=self.data["username"],
            password=self.data["password"],
            email=self.response_email_data["email"],
            login_provider=self.social_data["login_provider"],
            provider_key=self.mock.user_data["provider_key"],
        )
        # Add an email to the provider result.
        self.mock.user_data.update(self.response_email_data)
        validate_token_mock.return_value = self.mock
        # Obtain a token pair.
        response = SocialUserTokenObtainPair(self.data).handle()

        # Validate result.
        self.assert_token(response)
        # Make sure that not new user was created.
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(login_provider=self.data["login_provider"])
        self.assertEqual(user.provider_key, self.mock.user_data["provider_key"])
        self.assertEqual(user, temp_user)
        # Make sure that a user can log in with his own password.
        self.assertTrue(check_password(self.data["password"], user.password))
        self.assertTrue(user.has_usable_password())

    def test_update_social_data(self, validate_token_mock):
        temp_user = UserFactory(
            username=self.data["username"],
            password=self.data["password"],
            first_name="",
            last_name="",
        )
        # Add an email, first name and last name to the provider result.
        self.mock.user_data.update(self.response_email_data)
        self.mock.user_data.update(self.response_user_names)
        validate_token_mock.return_value = self.mock
        # Obtain a token pair.
        response = SocialUserTokenObtainPair(self.data).handle()
        # Validate result.
        self.assert_token(response)
        # Make sure that not new user was created.
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(login_provider=self.data["login_provider"])
        self.assertEqual(user.provider_key, self.mock.user_data["provider_key"])
        self.assertEqual(user, temp_user)
        self.assertEqual(user.email, self.response_email_data["email"])
        self.assertEqual(user.first_name, self.response_user_names["first_name"])
        self.assertEqual(user.last_name, self.response_user_names["last_name"])

    def test_update_social_data_first_last_names_not_updated(self, validate_token_mock):
        temp_user = UserFactory(
            username=self.data["username"],
            password=self.data["password"],
            first_name="A",
            last_name="B",
        )
        # Add an email, first name and last name to the provider result.
        self.mock.user_data.update(self.response_email_data)
        self.mock.user_data.update(self.response_user_names)
        validate_token_mock.return_value = self.mock
        # Obtain a token pair.
        response = SocialUserTokenObtainPair(self.data).handle()
        # Validate result.
        self.assert_token(response)
        # Make sure that not new user was created.
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(login_provider=self.data["login_provider"])
        self.assertEqual(user.provider_key, self.mock.user_data["provider_key"])
        self.assertEqual(user, temp_user)
        self.assertEqual(user.email, self.response_email_data["email"])
        # Name weren't updated.
        self.assertNotEqual(user.first_name, self.response_user_names["first_name"])
        self.assertNotEqual(user.last_name, self.response_user_names["last_name"])

    @override_settings(SOCIAL_PROVIDERS=None)
    def test_social_provider_settings_are_not_set(self, validate_token_mock):
        with self.assertRaises(ValueError) as context:
            SocialUserTokenObtainPair(self.data).handle()
            self.assertTrue("SOCIAL_PROVIDERS setting is not set" in context.exception)

    def test_fail_on_wrong_login_provider(self, validate_token_mock):
        self.data["login_provider"] = "wrong"
        # Try to obtain a token pair.
        response = SocialUserTokenObtainPair(self.data).handle()

        self.assertTrue(response.data["message"])
        self.assertEqual(
            response.data["code"],
            str(settings.FRIENDLY_EXCEPTION_DICT["MethodNotAllowed"]),
        )
        self.assertEqual(response.status_code, 400)

    def test_fail_on_provider_error(self, validate_token_mock):
        self.mock.user_data = None
        self.mock.error_msg = "Login provider Error"
        self.mock.status = ProviderResult.STATUS.ERROR
        self.mock.ok.return_value = False
        validate_token_mock.return_value = self.mock

        # Try to obtain a token pair.
        response = SocialUserTokenObtainPair(self.data).handle()

        self.assertTrue(response.data["message"])
        self.assertEqual(
            response.data["code"],
            str(settings.FRIENDLY_EXCEPTION_DICT["AuthenticationFailed"]),
        )
        self.assertEqual(response.status_code, 400)
