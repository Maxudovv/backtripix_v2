from typing import Any, Dict

from app.models import Region


def region_to_dict(region: Region) -> Dict[str, Any]:
    return dict(id=region.id, name=region.name, country=region.country.code)
