from django.urls import path

from auth.api.v0.views.token import ConnectTokenView
from auth.api.v0.views.user_info import UserInfoAPIView

urlpatterns = [
    path("connect/token/", ConnectTokenView.as_view(), name="token_obtain_pair"),
    path("user/info", UserInfoAPIView.as_view(), name="user-info"),
]
