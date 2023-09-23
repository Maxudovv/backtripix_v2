from django.urls import include, path

urlpatterns = [
    path("v0/", include(("auth.api.v0.urls", "auth"), namespace="v0"), name="v0")
]
