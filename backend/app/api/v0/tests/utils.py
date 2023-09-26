from typing import Any, Dict

from app.models import Project, Region
from common.models import LANGUAGE


def region_to_dict(region: Region) -> Dict[str, Any]:
    return dict(id=region.id, name=region.name, country=region.country.code)


def project_to_dict(project: Project, language: LANGUAGE) -> Dict[str, Any]:
    return dict(
        id=project.id,
        name=getattr(
            project.translations.filter(language=language).last(), "name", None
        ),
        region=project.region_id,
        media=[
            dict(
                image_url=f"http://testserver{media.original_image.url}",
            )
            for media in project.media.all()
        ],
    )
