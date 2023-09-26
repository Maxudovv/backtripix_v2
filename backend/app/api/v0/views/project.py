from django.db.models import OuterRef, QuerySet, Subquery
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ReadOnlyModelViewSet

from app.api.v0.serializers.project_serializer import (
    ProjectItemSerializer,
    ProjectListSerializer,
)
from app.models.project import Project, ProjectStatus, ProjectTranslation


class ProjectViewSet(ReadOnlyModelViewSet):
    queryset = Project.objects.filter(status=ProjectStatus.active)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ["region"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProjectItemSerializer
        return ProjectListSerializer

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()

        queryset = self.annotate_translation_fields(queryset)
        queryset = queryset.prefetch_related("media")
        return queryset

    def annotate_translation_fields(self, queryset: QuerySet) -> QuerySet:
        return queryset.annotate(
            name=Subquery(
                ProjectTranslation.objects.filter(
                    project=OuterRef("pk"), language=self.request.user.language
                ).values_list("name")
            )
        ).distinct("id")
