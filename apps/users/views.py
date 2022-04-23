from rest_framework.generics import RetrieveAPIView
from users.models import User
from users.serializers import UserSerializer


class UserView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
