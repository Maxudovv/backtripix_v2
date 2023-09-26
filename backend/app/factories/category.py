import factory
from factory import SubFactory
from factory.django import DjangoModelFactory

from app.models.category import Category, CategoryTranslation
from common.models import LANGUAGE


class CategoryFactory(DjangoModelFactory):
    name = factory.Faker("word")

    class Meta:
        model = Category


class CategoryTranslationFactory(DjangoModelFactory):
    name = factory.Faker("word")
    language = LANGUAGE.EN
    category = SubFactory(CategoryFactory)

    class Meta:
        model = CategoryTranslation
