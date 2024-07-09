from rest_framework.views import APIView
from catalog.models import Lesson
from catalog.serializers import LessonSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from catalog.permissions.student_permissions import HasLessonAccess
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema


class LessonView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser, ]

    @swagger_auto_schema(request_body=LessonSerializer)
    def post(self, request):
        input_serializer = LessonSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        user = request.user
        if user.is_staff:
            input_serializer.save()
            return Response()
        else:
            raise PermissionDenied("Only staff users can add lesson.")

    def get(self, request):
        queryset = Lesson.objects.all()
        serializer = LessonSerializer(queryset, many=True)
        return Response(serializer.data)


class LessonViewSet(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), HasLessonAccess()]
        elif self.request.method == 'PUT':
            return [IsAuthenticated(), IsAdminUser()]
        elif self.request.method == 'DELETE':
            return [IsAuthenticated(), IsAdminUser()]
        return []

    def get(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)
        serializer = LessonSerializer(lesson)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=LessonSerializer)
    def put(self, request, lesson_id):
        user = request.user
        if user.is_staff:
            lesson = get_object_or_404(Lesson, id=lesson_id)
            input_serializer = LessonSerializer(instance=lesson, data=request.data)
            input_serializer.is_valid(raise_exception=True)
            input_serializer.save()
            return Response()
        else:
            raise PermissionDenied("Only staff users can update lesson.")

    def delete(self, request, lesson_id):
        user = request.user
        if user.is_staff:
            get_object_or_404(Lesson, id=lesson_id).delete()
            return Response()
        else:
            raise PermissionDenied("Only staff users can delete lesson.")
