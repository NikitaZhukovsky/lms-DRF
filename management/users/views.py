from djoser.views import UserViewSet
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.serializers import CustomUserSerializer, UserViewSerializer
from users.models import CustomUser
from rest_framework import status
from django.http import JsonResponse


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
        email = request.data.get("email")
        admin = request.user
        if admin.is_staff:
            try:
                user = CustomUser.objects.get(email=email)
                input_serializer = CustomUserSerializer(user, data=request.data, partial=True)
                if input_serializer.is_valid():
                    input_serializer.save()
                    return Response(input_serializer.data)
                else:
                    return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except CustomUser.DoesNotExist:
                raise status.HTTP_404_NOT_FOUND
        else:
            raise PermissionDenied("Only admin users can update other users roles.")


class TeacherView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = CustomUser.objects.filter(role='Teacher')
    serializer_class = UserViewSerializer


class StudentView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = CustomUser.objects.filter(role='Student')
    serializer_class = UserViewSerializer



