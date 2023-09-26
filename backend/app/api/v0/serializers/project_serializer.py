from rest_framework import serializers

from app.models import Project, ProjectMedia


class ProjectMediaSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProjectMedia
        fields = ("image_url",)

    def get_image_url(self, media: ProjectMedia) -> str:
        request = self.parent.context["request"]
        return request.build_absolute_uri(media.original_image.url)


class ProjectListSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    media = ProjectMediaSerializer(many=True)

    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "region",
            "media",
        )


class ProjectItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id",)
