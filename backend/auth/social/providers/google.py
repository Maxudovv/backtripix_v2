from typing import Any, Dict

from auth.social.providers.base import BaseAuth
from auth.social.providers.results import ProviderResult
from common.utils import str2bool


class GoogleOauth(BaseAuth):
    API_VERSION = "2"
    ACCESS_TOKEN_URL = "https://oauth2.googleapis.com/tokeninfo"

    def __init__(self):
        super().__init__()

    def check_settings(self):
        """No need APP_ID and APP_SECRET to verify an acces_token."""

    def get_request_url(self, token: str) -> str:
        return f"{self.ACCESS_TOKEN_URL}?id_token={token}"

    def handle_response(self, response: Dict[str, Any]) -> ProviderResult:
        if "error" in response:
            return ProviderResult(
                status=ProviderResult.STATUS.ERROR,
                error_msg=response["error"],
            )
        return ProviderResult(
            status=ProviderResult.STATUS.SUCCESS,
            user_data=self.get_user_data(response),
        )

    def get_user_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = {"provider_key": data["sub"]}
        if {"email_verified", "email"} <= data.keys() and str2bool(
            data["email_verified"]
        ):
            result.update({"email": data["email"]})
        if {"given_name", "family_name"} <= data.keys():
            result.update(
                {"first_name": data["given_name"], "last_name": data["family_name"]}
            )
        if "picture" in data.keys():
            result.update({"avatar": data["picture"]})
        return result
