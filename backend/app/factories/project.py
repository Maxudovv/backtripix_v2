import factory
from factory import SubFactory
from factory.django import DjangoModelFactory, ImageField

from app.factories.region import RegionFactory
from app.models import Project, ProjectMedia, ProjectStatus, ProjectTranslation
from common.models import LANGUAGE


class ProjectFactory(DjangoModelFactory):
    status = ProjectStatus.active
    region = SubFactory(RegionFactory)

    class Meta:
        model = Project


class ProjectTranslationFactory(DjangoModelFactory):
    project = SubFactory(ProjectFactory)
    name = factory.Faker("word")
    language = LANGUAGE.EN

    class Meta:
        model = ProjectTranslation


class ProjectMediaFactory(DjangoModelFactory):
    class Meta:
        model = ProjectMedia

    project = SubFactory(ProjectFactory)
    original_image = ImageField(width=1920, height=1200)
