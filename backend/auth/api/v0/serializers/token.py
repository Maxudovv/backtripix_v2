import jwt
from django.conf import settings
from rest_framework import serializers
from rest_framework_simplejwt import serializers as simplejwt_serializers
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from auth.models import User
from auth.utils import is_valid_email


class TokenObtainPairSerializer(simplejwt_serializers.TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # For Swagger
        self.fields["access_token"] = serializers.CharField(default="")
        self.fields["login_provider"] = serializers.CharField(default="")

    def validate(self, attrs):
        try:
            return super().validate(attrs)
        # A user has not been found by username.
        except AuthenticationFailed as exc:
            # Check if username is email.
            username = attrs[self.username_field]
            if not is_valid_email(username):
                raise exc
            # Try to find a user by email.
            user = User.objects.filter(email__exact=username).first()
            if not self.can_authorize(user):
                raise exc
            # Set the user's real username to attrs.
            attrs[self.username_field] = user.username
            return super().validate(attrs)

    def can_authorize(self, user):
        return user and user.is_active

    def to_representation(self, instance):
        return {
            "resource": "resource_server",
            "scope": "openid email profile offline_access",
            "token_type": "Bearer",
            "access_token": self.validated_data["access"],
            "expires_in": settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds(),
            "refresh_token": self.validated_data["refresh"],
            "id_token": jwt.encode({"is_temp": "true"}, "secret", algorithm="HS256"),
        }

    class Meta:
        ref_name = "TokenObtainPairSerializerV2"


class TokenRefreshSerializer(simplejwt_serializers.TokenRefreshSerializer):
    def to_internal_value(self, data):
        data = data.copy()
        data["refresh"] = data["refresh_token"]
        return super().to_internal_value(data)

    def validate(self, attrs):
        data = super().validate(attrs)
        # check user is active
        token_data = self.token_class(attrs["refresh"])
        user_id = token_data.get("user_id")
        user = User.objects.filter(id=user_id).last()
        if not (user and user.is_active):
            raise AuthenticationFailed
        if "refresh" not in data:
            data["refresh"] = attrs["refresh"]
        return data

    def to_representation(self, instance):
        return {
            "token_type": "Bearer",
            "access_token": self.validated_data["access"],
            "refresh_token": self.validated_data["refresh"],
            "expires_in": settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds(),
            "id_token": jwt.encode({"is_temp": "true"}, "secret", algorithm="HS256"),
        }

    class Meta:
        ref_name = "TokenRefreshSerializerV2"
