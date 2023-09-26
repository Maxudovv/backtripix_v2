from django.urls import include, path

urlpatterns = [
    path("v0/", include(("app.api.v0.urls", "app"), namespace="v0"), name="v0")
]
