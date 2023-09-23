from django.utils.translation import activate
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Get (user, token) or None
        result = super().authenticate(request)
        if result is None:
            return result
        user, token = result
        if user:
            activate(user.language)
        return result
