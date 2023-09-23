from rest_framework import serializers

from auth.api.v0.serializers.region import RegionSerializer
from auth.models import User


class UserInfoSerializer(serializers.ModelSerializer):
    region = RegionSerializer()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "language",
            "region",
        )
