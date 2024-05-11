from djoser.views import UserViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.serializers import CustomUserSerializer
from users.models import CustomUser
from rest_framework import status
from django.http import JsonResponse


def get_csrf_token(request):
    return JsonResponse({'csrfToken': request.csrf_token})


class ActivateUser(UserViewSet):

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())

        kwargs['data'] = {
            'uid': self.kwargs['uid'],
            'token': self.kwargs['token']
        }

        return serializer_class(*args, **kwargs)


class AddTeacherView(APIView):
    permission_classes = (IsAuthenticated, )

    def patch(self, request):
        input_serializer = CustomUserSerializer(data=request.data)
        if input_serializer.is_valid():
            try:
                user = CustomUser.objects.get(email=input_serializer.validated_data["email"])
                new_role = input_serializer.validated_data.get("role")
                user.role = new_role
                user.save()
                return Response(input_serializer.data)
            except CustomUser.DoesNotExist:
                raise status.HTTP_404_NOT_FOUND
        else:
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


