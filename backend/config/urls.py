from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg2 import openapi
from drf_yasg2.views import get_schema_view
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

schema_view = get_schema_view(
    openapi.Info(
        title="Tripix API",
        default_version="v2",
        description="API for all things …",
    ),
    public=False,
    authentication_classes=(SessionAuthentication,),
    permission_classes=(IsAuthenticated,),
    url="https://tripix.site",
)

urlpatterns = [
    path(
        "docs/private/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("admin/", admin.site.urls),
    path(
        "auth-service/",
        include(("auth.urls", "auth"), namespace="auth-service"),
        name="auth-service",
    ),
    path(
        "app-service/",
        include(("app.urls", "app"), namespace="app-service"),
        name="app-service",
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DJANGO_SILK_ENABLED:
    urlpatterns += [url(r"^silk/", include("silk.urls", namespace="silk"))]
