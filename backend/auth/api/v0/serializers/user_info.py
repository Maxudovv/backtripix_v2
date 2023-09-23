from rest_framework import serializers

from app.models import Region
from auth.api.v0.serializers.region import RegionSerializer
from auth.models import User


class UserInfoSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    region_id = serializers.PrimaryKeyRelatedField(
        queryset=Region.objects.filter(status=Region.STATUS.ACTIVE),
        source="region.id",
        write_only=True,
    )

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
            "region_id",
        )

    def update(self, instance, validated_data):
        if region := validated_data.pop("region", None):
            instance.region = region["id"]
        return super().update(instance, validated_data)
