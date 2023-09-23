import factory
from factory import SubFactory
from factory.django import DjangoModelFactory

from app.factories.country import CountryFactory
from app.models import Region


class RegionFactory(DjangoModelFactory):
    class Meta:
        model = Region

    country = SubFactory(CountryFactory)
    name = factory.Faker("word")
    status = factory.Sequence(lambda _: Region.STATUS.ACTIVE)
