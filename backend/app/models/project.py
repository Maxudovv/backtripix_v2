from django.db import models
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit

from app.models.category import Category
from app.models.region import Region
from app.utils import RemoveExifData, upload_to
from common.base_models import ModelWithGeo
from common.models import LANGUAGE
from config import settings


class ProjectStatus(models.IntegerChoices):
    pending = 0
    active = 1
    closed = 2
    archive = 3


class Project(ModelWithGeo):
    status = models.PositiveSmallIntegerField(
        choices=ProjectStatus.choices, default=ProjectStatus.pending
    )
    categories = models.ManyToManyField(Category, related_name="projects")
    region = models.ForeignKey(
        Region, on_delete=models.PROTECT, related_name="projects"
    )

    # Meta fields
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    def __str__(self):
        return getattr(self.translations.last(), "name", super().__str__())


class ProjectTranslation(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="translations",
    )
    language = models.CharField(max_length=2, choices=LANGUAGE.CHOICES)
    name = models.CharField(max_length=100)


class ProjectMedia(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name="media")

    original_image = ProcessedImageField(
        upload_to=upload_to,
        null=True,
        blank=True,
        format="JPEG",
        options={"quality": settings.UPLOAD_MEDIA_IMAGE_QUALITY},
        processors=[
            ResizeToFit(width=1920, height=1200, upscale=False),
            RemoveExifData(),
        ],
    )
