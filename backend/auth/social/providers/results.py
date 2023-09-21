from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ProviderResult:
    class STATUS:
        SUCCESS = 0
        ERROR = 1

    status: int
    # In case of success, user_data should contain a user data
    user_data: Optional[Dict[str, Any]] = None
    # In case of an error, error string should be non empty
    error_msg: Optional[str] = None

    def ok(self) -> bool:
        if self.status == self.STATUS.SUCCESS and self.user_data:
            return True
        return False
