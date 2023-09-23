from rest_framework.generics import RetrieveAPIView, UpdateAPIView

from auth.api.v0.serializers.user_info import UserInfoSerializer
from auth.models import User


class UserInfoAPIView(RetrieveAPIView, UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer

    def get_object(self):
        return self.request.user
