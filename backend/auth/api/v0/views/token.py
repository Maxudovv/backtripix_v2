from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt import exceptions as simplejwt_exceptions
from rest_framework_simplejwt.views import TokenObtainPairView

from auth.api.v0 import serializers
from auth.api.v0.serializers import TokenObtainPairSerializer
from auth.social.token import SocialUserTokenObtainPair


class ConnectTokenView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def get_serializer(self, *args, **kwargs):
        data = kwargs.get("data", None)
        if data and "refresh_token" in data:
            return serializers.TokenRefreshSerializer(*args, **kwargs)
        return serializers.TokenObtainPairSerializer(*args, **kwargs)

    # There is a tiny bug in post method in TokenViewBase, it uses validated_data
    # instead of data which ignores to_representation.
    def post(self, request, *args, **kwargs):
        # Copy the request data.
        request_data = request.data.copy()

        IS_SOCIAL_LOGIN = {"login_provider", "access_token"} <= request_data.keys()

        # Check if username and password or refresh_token or
        # login_provider and access_token exist in request data
        if not (
            {"username", "password"} <= request_data.keys()
            or "refresh_token" in request_data
            or IS_SOCIAL_LOGIN
        ):
            raise simplejwt_exceptions.AuthenticationFailed(
                "Specify either 'username' with 'password' or "
                "'refresh_token' or "
                "'login_provider' with 'access_token' in the request"
            )

        if IS_SOCIAL_LOGIN:
            return SocialUserTokenObtainPair(request_data).handle()

        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except simplejwt_exceptions.TokenError as e:
            raise simplejwt_exceptions.InvalidToken(e.args[0])

        return Response(serializer.data, status=status.HTTP_200_OK)
