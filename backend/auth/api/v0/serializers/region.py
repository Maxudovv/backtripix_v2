from rest_framework import serializers

from app.models import Region


class RegionSerializer(serializers.ModelSerializer):
    country = serializers.CharField(max_length=2, source="country__code")

    class Meta:
        model = Region
        fields = ("name", "country")
