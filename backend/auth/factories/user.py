import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory, ImageField


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: f"user {n}")
    first_name = factory.Sequence(lambda n: f"first_name {n}")
    last_name = factory.Sequence(lambda n: f"last_name {n}")
    password = factory.PostGenerationMethodCall("set_password", "qwerty123")
    email = factory.Sequence(lambda n: f"email-{n}@gmail.com")
    region = factory.SubFactory("app.factories.region.RegionFactory")
    original_avatar = ImageField(color="red", width=600, height=600)
