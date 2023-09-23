from django.urls import include, path

urlpatterns = [
    path("api/", include(("auth.api.urls", "auth"), namespace="api"), name="api")
]
