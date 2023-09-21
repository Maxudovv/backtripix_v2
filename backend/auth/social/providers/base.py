import abc
import logging
from typing import Any, Dict

import httpx

from auth.social.providers.results import ProviderResult

logger = logging.getLogger(__name__)


class BaseAuth(abc.ABC):
    """Base provider class."""

    def __init__(self):
        # Make sure that the settings are set
        self.check_settings()

    def make_request(self, token: str):
        url = self.get_request_url(token)
        return httpx.get(url)

    def validate_token(self, token: str) -> ProviderResult:
        # Make a request to the social site token checking endpoint.
        response = self.make_request(token)

        if response.status_code != 200:
            error_msg = (
                f"Status: {response.status_code}, "
                f"Reason: {response.reason_phrase}, "
                f"Text: {response.text}"
            )
            logger.error(error_msg)
            return ProviderResult(
                status=ProviderResult.STATUS.ERROR,
                error_msg=error_msg,
            )
        json_response = response.json()
        # Process the response.
        return self.handle_response(json_response)

    @abc.abstractmethod
    def check_settings(self):
        """Check settings for a corresponding provider."""

    @abc.abstractmethod
    def get_request_url(self, token: str) -> str:
        """Get token checking URL for corresponding provider."""

    @abc.abstractmethod
    def handle_response(self, response: Dict[str, Any]) -> ProviderResult:
        """Get user data from token check response."""
