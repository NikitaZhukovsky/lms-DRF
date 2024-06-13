from djoser.views import UserViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import IsAuthenticated
from users.serializers import CustomUserSerializer, UserViewSerializer, UserUpdateSerializer
from users.models import CustomUser
from rest_framework import status, viewsets
from rest_framework import generics


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
            raise PermissionDenied("Only staff users can update other users roles.")


class TeacherViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserViewSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.role == 'Teacher':
            return CustomUser.objects.filter(role='Teacher')
        else:
            raise PermissionDenied("Only admin users and Teachers can view all teachers.")

    def retrieve(self, request, pk=None):
        try:
            teacher = self.get_queryset().get(pk=pk)
            serializer = self.serializer_class(teacher)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            raise NotFound(f"No Teacher found with ID {pk}")


class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserViewSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.role == 'Teacher':
            return CustomUser.objects.filter(role='Student')
        else:
            raise PermissionDenied("Only admin users and Teachers can view all students.")

    def retrieve(self, request, pk=None):
        try:
            student = self.get_queryset().get(pk=pk)
            serializer = self.serializer_class(student)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            raise NotFound(f"No Teacher found with ID {pk}")


class UserUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        if self.get_object() != self.request.user:
            raise PermissionDenied("You can only update your own profile.")
        serializer.save()


