from typing import Any, Dict

from app.api.v0.tests.utils import region_to_dict
from auth.models import User


def user_to_dict(user: User) -> Dict[str, Any]:
    return dict(
        id=user.id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        language=user.language,
        region=region_to_dict(user.region) if user.region else None,
    )
