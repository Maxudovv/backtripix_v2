from rest_framework.routers import SimpleRouter

from app.api.v0.views.project import ProjectViewSet

router = SimpleRouter()
router.register(prefix="projects", viewset=ProjectViewSet, basename="projects")

urlpatterns = router.urls + []
