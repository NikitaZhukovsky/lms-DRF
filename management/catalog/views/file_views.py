from catalog.models import LessonContent, CourseImage
from catalog.serializers import LessonContentSerializer, CourseImageSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import FileResponse
from catalog.permissions.student_permissions import HasLessonContentAccess
from catalog.tasks import delete_lesson_content, add_lesson_content
from django.core.files.storage import default_storage


class LessonContentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, HasLessonContentAccess]
    queryset = LessonContent.objects.all()
    serializer_class = LessonContentSerializer
    parser_classes = (MultiPartParser, FormParser)
    http_method_names = ['get', 'post', 'head', 'options', 'delete']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        response = FileResponse(instance.file, as_attachment=True, filename=instance.file.name)
        return response

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data

        for data in response_data:
            data['file'] = request.build_absolute_uri(data['file'])

        return Response(response_data)

    def create(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated, IsAdminUser]
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        lesson_id = serializer.validated_data['lesson'].id

        response_data = serializer.data
        response_data['file'] = request.build_absolute_uri(response_data['file'])
        headers = self.get_success_headers(serializer.data)
        add_lesson_content(lesson_id)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated, IsAdminUser]
        instance = self.get_object()
        lesson_id = instance.lesson_id
        if instance.file:
            default_storage.delete(instance.file.name)
        delete_lesson_content(lesson_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseImageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = CourseImage.objects.all()
    serializer_class = CourseImageSerializer
    parser_classes = (MultiPartParser, FormParser)
    http_method_names = ['get', 'post', 'head', 'options', 'delete']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        response = FileResponse(instance.file, as_attachment=True, filename=instance.file.name)
        return response

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data

        for data in response_data:
            data['file'] = request.build_absolute_uri(data['file'])

        return Response(response_data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_data = serializer.data
        response_data['file'] = request.build_absolute_uri(response_data['file'])
        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated, IsAdminUser]
        instance = self.get_object()
        if instance.file:
            default_storage.delete(instance.file.name)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
