from factory.django import DjangoModelFactory

from app.models import Country


class CountryFactory(DjangoModelFactory):
    code = "RU"

    class Meta:
        model = Country
        django_get_or_create = ("code",)
