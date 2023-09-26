from django.urls import reverse
from rest_framework import status

from app.api.v0.tests.utils import project_to_dict
from app.factories import ProjectFactory, ProjectTranslationFactory
from app.factories.project import ProjectMediaFactory
from auth.factories.user import UserFactory
from common.models import LANGUAGE
from common.rest_framework.testing import BaseTestCase


class ProjectTestCase(BaseTestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.jwt_authenticate(self.user)

        self.project = ProjectFactory(region=self.user.region)
        for language in LANGUAGE.CHOICES:
            ProjectTranslationFactory(project=self.project, language=language[0])

        ProjectMediaFactory(project=self.project)

        self.url = reverse("app-service:api:v0:projects-list")
        return

    def test_url(self):
        self.assertEqual(self.url, "/app-service/api/v0/projects/")

    def test_get_projects(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0],
            project_to_dict(self.project, language=self.user.language),
        )

    def test_wrong_region_filter(self):
        response = self.client.get(self.add_params(self.url, region=100))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_region_filter(self):
        project = ProjectFactory()  # New region creates here
        response = self.client.get(self.add_params(self.url, region=project.region.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0],
            project_to_dict(project, language=self.user.language),
        )
