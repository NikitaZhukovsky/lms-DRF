from catalog.models import Course, CourseModule, Lesson, LessonContent, StudentCourse, CourseImage
from catalog.serializers import (CourseSerializer, CourseModuleSerializer,
                                 LessonSerializer, LessonContentSerializer,
                                 StudentCourseSerializer, CourseImageSerializer)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import FileResponse
from catalog.permissions.student_permissions import HasModuleAccess, HasLessonAccess, HasLessonContentAccess


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.is_staff:
            return super().create(request, *args, **kwargs)
        else:
            raise PermissionDenied("Only staff users can add courses.")

    def update(self, request, *args, **kwargs):
        user = request.user
        if user.is_staff:
            return super().update(request, *args, **kwargs)
        else:
            raise PermissionDenied("Only staff users can update courses.")

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if user.is_staff:
            return super().destroy(request, *args, **kwargs)
        else:
            raise PermissionDenied("Only staff users can delete courses.")


class CourseModuleViewSet(viewsets.ModelViewSet):
    queryset = CourseModule.objects.all()
    serializer_class = CourseModuleSerializer
    permission_classes = [IsAuthenticated, HasModuleAccess]

    def create(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated, IsAdminUser]
        user = request.user
        if user.is_staff:
            return super().create(request, *args, **kwargs)
        else:
            raise PermissionDenied("Only staff users can add modules.")

    def update(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated, IsAdminUser]
        user = request.user
        if user.is_staff:
            return super().update(request, *args, **kwargs)
        else:
            raise PermissionDenied("Only staff users can update modules.")

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated, IsAdminUser]
        user = request.user
        if user.is_staff:
            return super().destroy(request, *args, **kwargs)
        else:
            raise PermissionDenied("Only staff users can delete modules.")


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, HasLessonAccess]

    def create(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated, IsAdminUser]
        user = request.user
        if user.is_staff:
            return super().create(request, *args, **kwargs)
        else:
            raise PermissionDenied("Only staff users and teachers can add lessons.")

    def update(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated, IsAdminUser]
        user = request.user
        if user.is_staff:
            return super().update(request, *args, **kwargs)
        else:
            raise PermissionDenied("Only staff users and teachers can update lessons.")

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated, IsAdminUser]
        user = request.user
        if user.is_staff:
            return super().destroy(request, *args, **kwargs)
        else:
            raise PermissionDenied("Only staff users and teachers can delete lessons.")


class StudentCourseViewSet(viewsets.ModelViewSet):
    queryset = StudentCourse.objects.all()
    serializer_class = StudentCourseSerializer
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.is_staff:
            input_serializer = self.get_serializer(data=request.data)
            input_serializer.is_valid(raise_exception=True)
            student = input_serializer.validated_data['student']
            student.role = 'Student'
            student.save()
            input_serializer.save()
            return Response()
        else:
            raise PermissionDenied("Only staff users can add students to courses.")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_student_courses(self, request, student_id, *args, **kwargs):
        try:
            student_courses = StudentCourse.objects.filter(student_id=student_id)
            serializer = self.get_serializer(student_courses, many=True)
            return Response(serializer.data)
        except StudentCourse.DoesNotExist:
            raise NotFound(f"No student-course relationships found for student with ID {student_id}")

    def delete_student_from_course(self, request, student_id):
        try:
            student_courses = StudentCourse.objects.filter(student_id=student_id)
            student_courses.delete()
            return Response(status=204)
        except StudentCourse.DoesNotExist:
            raise NotFound(f"No student-course relationships found for student with ID {student_id}")


class LessonContentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, HasLessonContentAccess]
    queryset = LessonContent.objects.all()
    serializer_class = LessonContentSerializer
    parser_classes = (MultiPartParser, FormParser)

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
        response_data = serializer.data
        response_data['file'] = request.build_absolute_uri(response_data['file'])
        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated, IsAdminUser]
        instance = self.get_object()
        instance.file.delete(False)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseImageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = CourseImage.objects.all()
    serializer_class = CourseImageSerializer
    parser_classes = (MultiPartParser, FormParser)

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
        instance = self.get_object()
        instance.file.delete(False)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
