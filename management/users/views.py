from djoser.views import UserViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class ActivateUser(UserViewSet):

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())

        kwargs['data'] = {
            'uid': self.kwargs['uid'],
            'token': self.kwargs['token']
        }

        return serializer_class(*args, **kwargs)
